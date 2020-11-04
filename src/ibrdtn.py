import socket

from time import sleep
from environs import Env


class IbrdtnDaemon:
    def __init__(self):
        env = Env()
        env.read_env()
        self._DTN_DAEMON_ADDRESS = env.str("DTN_DAEMON_ADDRESS")
        self._DTN_DAEMON_PORT = env.int("DTN_DAEMON_PORT")
        self._DTN_APP = env.str("DTN_APP")
        self.daemon_socket = None
        self.daemon_stream = None

    def create_connection(self):
        """
          Attempts to create a connection to IBRDTN daemon, if it fails, takes a
          5 seconds interval until next try.
        """
        connected = False

        while not connected:
            try:
                print("Trying to connect to IBRDTN daemon...")
                self._connect_to_daemon()
                connected = True
                print("Trying to connect to IBRDTN daemon... CONNECTED!")
            except ConnectionError:
                sleep(5)

    def _connect_to_daemon(self):
        """
            Creates a socket and a stream (file object aka file descriptor)
            to communicate with DTN daemon. Sets the daemon in protocol extended
            mode and the endpoint app source.
            """
        try:
            # Create the socket to communicate with the DTN daemon
            self.daemon_socket = socket.socket()
            # Connect to the DTN daemon
            self.daemon_socket.connect(
                (self._DTN_DAEMON_ADDRESS, self._DTN_DAEMON_PORT)
            )
            # Get a file object associated with the daemon's socket
            self.daemon_stream = self.daemon_socket.makefile()
            # Read daemon's header response
            self.daemon_stream.readline()
            # Switch to extended protocol mode
            self.daemon_socket.send(b"protocol extended\n")
            # Read protocol switch response
            self.daemon_stream.readline()
            # Set endpoint identifier
            self.daemon_socket.send(
                bytes("set endpoint %s\n" % self._DTN_APP, encoding="UTF-8")
            )
            # Read protocol set EID response
            self.daemon_stream.readline()

        except ConnectionError as error:
            raise ConnectionError(
                "Failed to create a socket and stream to the IBRDTN daemon.\n",
                error,
            )

    def close_connection(self):
        """
        Closes stream (file descriptor) and socket to IBTDTN daemon.
        """
        if self.daemon_stream is not None:
            self.daemon_stream.close()

        if self.daemon_socket is not None:
            self.daemon_socket.close()
