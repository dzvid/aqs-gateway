import requests

from environs import Env


class Api:
    """
    Class to abstract API endpoints.
    """

    def __init__(self):
        env = Env()
        env.read_env()
        self._API_URL = env.str("API_URL")

    def _url(self, path):
        return self._API_URL + path

    def store_reading(self, sensor_node_id, reading):
        """
        Sends a sensor node reading to be persisted by API.

        Parameters
        ----------
        sensor_node_id : string
          A sensor node's uuid.
        reading : JSON
          A sensor node's reading.
        """

        try:
            reading_endpoint = "/sensor-nodes/{0}/readings".format(
                sensor_node_id
            )
            response = requests.post(
                url=self._url(reading_endpoint), json=reading, timeout=5
            )

            if response.status_code == 201:
                print("Reading stored successfully!\n")
            else:
                print(
                    "Reading not stored!\nStatus:{0}\nResponse: {1}\n".format(
                        response.status_code, response.json()
                    )
                )
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as error:
            print("Failed to connect to the server: {0}".format(error))
        except Exception as error:
            print("Generic Error: {0}".format(error))
