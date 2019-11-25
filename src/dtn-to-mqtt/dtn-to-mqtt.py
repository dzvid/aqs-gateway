import socket
import paho.mqtt.client
import base64
import threading
import json
import queue as Queue

from environs import Env
from math import ceil
from pathlib import Path


# Functions to handle the communication with the DTN Daemon
def daemon_reader_thread(cv):
    """
    The reader thread fetches notifications of incoming bundles and responses to requests through the daemon's socket
    Args:
        cv: Condition variable used to protect access to global variables and to synchronize the main thread
    """
    global response
    global response_is_ready

    while True:
        remaining_lines = 0
        res = fd.readline().rstrip()
        if res.startswith("602 NOTIFY BUNDLE"):
            # Put the notification in a queue. The main thread will be responsible to process notifications.
            notifications.put(res)
            # No further processing is needed.
            continue
        elif res.startswith("200 BUNDLE LOADED"):
            remaining_lines = 0
        elif res.startswith("200 PAYLOAD GET"):
            remaining_lines = 3
        elif res.startswith("200 BUNDLE FREE"):
            remaining_lines = 0

        with cv:
            response = []
            for i in range(0, remaining_lines):
                response.append(fd.readline().rstrip())
            response.insert(0, res)

            if res.startswith("200 PAYLOAD GET"):
                # Further readings from daemon's socket to retrieve the actual payload of a bundle. The daemon's API
                # protocol replies with at most 80 characters per line and the payload is encoded in Base64.
                # So, the length of the payload (original, not encoded) is retrieved from the field "Length"
                # of the response. Then, the encoded length of the payload is calculated as ceil(length/3) * 4.
                # This number is further divided by 80 and rounded up in order to obtain how many lines has to be
                # read to retrieve the encoded payload.
                a = int(response[1].split()[1]) / 3.0
                b = ceil(a) * 4
                c = ceil(b / 80)
                # The plus 1 is due to a blank line after the encoded payload
                payload_lines = int(c) + 1
                response.append('')
                for i in range(0, payload_lines):
                    response[4] += fd.readline().rstrip()

            # Set the ready flag and wake up the main thread which is waiting for the response to a request
            response_is_ready = True
            cv.notify()


def wait_for_response(cv):
    """
    Synchronized read of the response to a request made to the DTN daemon
    Args:
        cv: Condition variable used to protect access to global variables and to synchronize the main thread
    Returns:
        a list containing all lines of the response read from the DTN daemon's socket
    """
    global response_is_ready

    with cv:
        while not response_is_ready:
            condition.wait()
        response_is_ready = False
        # Create an independent copy of the global variable 'response' to be returned to the caller,
        # because in the caller scope the global variable 'response' is no longer protected by the lock
        # and its value could change in order to reflect the changes made by the reader thread
        ret = response[:]

    return ret


# MQTT Callback methods
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker (RC: %s)" % rc)
    else:
        print("Connection to MQTT broker failed (RC: %s)" % rc)


def on_log(client, userdata, level, buf):
    print(buf)


def on_publish(client, userdata, mid):
    print("Data published (Mid: %s)" % mid)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnect")
    print("Disconnected from MQTT broker")

# JSON Validation method


def is_json(json_paylod):
    """
    Check if the payload is a valid json.
    Args: 
        json_paylod: The message payload send from the DTN node.
    """
    try:
        json_object = json.loads(json_paylod)
    except ValueError as e:
        return False
    return True


# Load enviroment variables
env = Env()
env_path = Path('.') / '.env'
env.read_env(path=env_path, recurse=False)

# Broker connection details
mqttBrokerHost = env('MQTT_BROKER_HOST')
mqttBrokerPort = env.int('MQTT_BROKER_PORT')
mqttUser = env('MQTT_USER')
mqttPassword = env('MQTT_PASS')

# DTN daemon connection details
DTN_DAEMON_ADDRESS = env('DTN_DAEMON_ADDRESS')
DTN_DAEMON_PORT = env.int('DTN_DAEMON_PORT')
# Demux token of this application, which will be concatenated with the DTN Endpoint identifier of the node
# where this script actually runs
DTN_SOURCE_DEMUX_TOKEN = env('DTN_SOURCE_DEMUX_TOKEN')


# Set MQTT client
mqttClient = paho.mqtt.client.Client()
mqttClient.username_pw_set(mqttUser, mqttPassword)
# Register callbacks
mqttClient.on_connect = on_connect
mqttClient.on_log = on_log
mqttClient.on_publish = on_publish
mqttClient.on_disconnect = on_disconnect
# Connect to MQTT broker
mqttClient.connect(mqttBrokerHost, mqttBrokerPort, 60)
# Start the network loop to process the communication with the broker in a separated thread
mqttClient.loop_start()

# Create the socket to communicate with the DTN daemon
d = socket.socket()
# Connect to the DTN daemon
d.connect((DTN_DAEMON_ADDRESS, DTN_DAEMON_PORT))
# Get a file object associated with the daemon's socket
fd = d.makefile()
# Read daemon's header response
fd.readline()
# Switch to extended protocol mode
d.send(b"protocol extended\n")
# Read protocol switch response
fd.readline()
# Set endpoint identifier
d.send(bytes("set endpoint %s\n" %
             DTN_SOURCE_DEMUX_TOKEN, encoding="UTF-8"))
# Read protocol set EID response
fd.readline()

# Create a worker thread that reads from daemon's socket for responses to requests or notifications of incoming bundles.
# Global variables 'response' and 'response_is_ready' will be manipulated by the worker thread once protected
# by the lock acquisition of the condition variable. The variable 'notifications' is a synchronized queue whose
# get and put methods are thread-safe.
response = []
response_is_ready = False
condition = threading.Condition()
notifications = Queue.Queue()
reader = threading.Thread(name='daemon_reader',
                          target=daemon_reader_thread, args=(condition,))
reader.start()

# Main thread loop:
# Retrieve and process notifications of incoming bundles, extract MQTT payload from the received bundle
# and finally publish the message to the broker.

while True:
    notification = notifications.get()
    query_string = notification.split(' ', 3)[3]
    d.send(bytes("bundle load %s\n" % query_string, encoding="UTF-8"))
    wait_for_response(condition)

    d.send(b"payload get\n")
    res = wait_for_response(condition)
    mqttData = str(base64.b64decode(res[4]), encoding="UTF-8")
    # the sensor topic and message are divided by one '\n'
    mqttData = mqttData.split('\n')
    mqttTopic = mqttData[0]
    mqttDataJson = mqttData[1]

    # Publish data
    try:
        if is_json(mqttDataJson):
            mqttClient.publish(
                topic=mqttTopic, payload=mqttDataJson, qos=1)
        else:
            raise ValueError(
                'Invalid payload provided, payload must be a JSON')
    except ValueError as valueError:
        print("Value Error: {}".format(valueError))
    except Exception as error:
        print("Generic Error: {}".format(error))

    d.send(b"bundle free\n")
    wait_for_response(condition)

    notifications.task_done()

mqttClient.loop_stop()
mqttClient.disconnect()
d.close()
