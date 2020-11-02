import requests


class Api:
    """
    Class to abstract API endpoints.
    """

    def __init__(self):
        self._BASE_URL = "http://localhost:3000"

    def _url(self, path):
        return self._BASE_URL + path

    def store_reading(self, reading):
        """
        Sends a sensor node reading to be persisted by API.

        Parameters
        ----------
        reading : JSON
          A sensor node reading.
        """

        try:
            response = requests.post(
                url=self._url("/readings"), json=reading, timeout=5
            )

            if response.status_code == 201:
                print("Reading stored successfully!\n")
            else:
                print(
                    "Reading not stored!\nStatus:{0}\nResponse: {1}\n".format(
                        response.status_code, response.json()
                    )
                )
        except (requests.ConnectionError, requests.Timeout) as error:
            print("Failed to connect to the server: {}".format(error))
        except Exception as error:
            print("Generic Error: {}".format(error))
