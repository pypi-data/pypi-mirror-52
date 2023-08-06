import requests

from sliceup.functions import *


class Sliceup:
    """Represents SliceUp client.

    :param host: Connection ip address
    :type host: str
    :param port: Connection port, defaults to '8080'
    :type port: str, optional
    """

    def __init__(self, host: str, port: str = '8080') -> None:
        """Creates a Sliceup client."""
        self.host = 'http://' + host + ':' + port + '/'

    def create(self, config: dict) -> requests.Response:
        """Creates the table with the given parameters in the database.

        :param config: New table configuration.
        """
        return self._post_request('create', config)

    def summary(self) -> requests.Response:
        """Summarizes the database configuration."""
        return self._get_request('summary')

    def insert(self, data: dict) -> requests.Response:
        """Inserts the given data into the database.

        :param data:
        :return:
        """
        return self._post_request('insert', data)

    def describe(self, name: str) -> requests.Response:
        """
        :param name:
        """
        return self._get_request('describe', {'name': name})

    def query(self, cmd: dict) -> Any:
        """Queries the database using the given parameters.

        :param cmd: Query parameters
        """
        self._process_args('select', cmd)
        self._process_args('by', cmd)
        self._process_from(cmd)
        result = self._post_request('query', cmd)
        return result.json()

    @staticmethod
    def _process_args(key: str, cmd: dict) -> dict:
        if key in cmd:
            selects = cmd[key]
            for i, expr in enumerate(selects):
                if isinstance(expr, str):
                    selects[i] = id(expr)

    @staticmethod
    def _process_from(cmd: dict) -> dict:
        f = cmd['from']
        if isinstance(f, str):
            cmd['from'] = {'Table': f}

    def _get_request(self, method, payload=None) -> requests.Response:
        result = requests.get(self.host + method, json=payload)
        return result

    def _post_request(self, method, payload=None) -> requests.Response:
        result = requests.post(self.host + method, json=payload)
        return result
