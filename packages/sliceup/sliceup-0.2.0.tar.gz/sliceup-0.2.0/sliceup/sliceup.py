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

    def delete(self, cmd: Union[str, list]) -> requests.Response:
        """Deletes requested tables from the database.

        :param cmd:
        :return:
        """
        cmd = _process_delete_args(cmd)
        return self._post_request('delete', cmd)

    def describe(self, name: str) -> requests.Response:
        """
        :param name:
        """
        return self._get_request('describe', {'name': name})

    def query(self, cmd: dict) -> Any:
        """Queries the database using the given parameters.

        :param cmd: Query parameters
        """
        _process_query_args(cmd)
        result = self._post_request('query', cmd)
        return result.json()

    def _get_request(self, method, payload=None) -> requests.Response:
        result = requests.get(self.host + method, json=payload)
        return result

    def _post_request(self, method, payload=None) -> requests.Response:
        result = requests.post(self.host + method, json=payload)
        return result

# Args processing


def _process_query_args(cmd: dict):
    column_args = ['select', 'where', 'by']
    for key in column_args:
        if key in cmd:
            cmd[key] = _to_args_array(cmd[key])
            for i in range(len(cmd[key])):
                cmd[key][i] = _to_id(cmd[key][i])

    from_key = 'from'
    if from_key in cmd:
        cmd[from_key] = _to_table(cmd[from_key])


def _process_delete_args(cmd: Union[str, list]):
    return _to_args_array(cmd)


def _to_args_array(cmd: Union[str, list]) -> list:
    if not isinstance(cmd, list):
        cmd = [cmd]
    return cmd


def _to_id(name: str) -> dict:
    if isinstance(name, str):
        name = {'Id': name}
    return name


def _to_table(name: str) -> dict:
    if isinstance(name, str):
        name = {'Table': name}
    return name
