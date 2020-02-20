
from datetime import datetime
from urllib.parse import urljoin

import requests

class PrometheusAPI:
    # TODO: enforce trailing slash for path?
    def __init__(self, endpoint='http://127.0.0.1:9090/', username=None, password=None):
        """

        :param endpoint: address of
        """
        self.endpoint = endpoint
        self.username = username
        self.password = password

    def _to_timestamp(self, input, base=None):
        """
        Convert string input to UNIX timestamp for Prometheus

        :param input:
        :param base:
        :return:
        """
        if type(input) == datetime:
            return input.timestamp()
        if input == 'now':
            return datetime.utcnow().timestamp()
        if type(input) in [int, float]:
            if input > 0:
                return input
            if input == 0:      # return now
                return datetime.utcnow().timestamp()
            if input < 0:
                base = self._to_timestamp(base)
                return base + input
        assert type(input) == float

        # TODO: test _to_timestamp('now') -> exists
        # TODO: test _to_timestamp(datetime.now()) -> exists
        # TODO: test _to_timestamp(52) -> exists
        # TODO: test _to_timestamp(52.4) -> exists
        # TODO: test _to_timestamp(-100, base=42) -> exists


    def query(self, query='prometheus_build_info'):
        return self._get(
            uri='api/v1/query',
            params=dict(
                query=query
            )
        )

    def query_range(self, query, start, end, step): #TODO timeout
        return self._get(
            uri='api/v1/query_range',
            params=dict(
                query=query,
                start=start,
                end=end,
                step=step
            )
        )

    def series(self, match='prometheus_build_info', start=-86400, end='now'):
        "Get ser"
        params = {
            'match[]': match
        }
        if end is not None:
            params['end'] = self._to_timestamp(end)
        if start:
            params['start'] = self._to_timestamp(start, base=end)
        return self._get(
            uri='api/v1/series',
            params= params
        )

    def labels(self, match='prometheus_build_info', start=-86400, end='now'):
        "Get labels"
        params = {
            'match[]': match
        }
        if end is not None:
            params['end'] = self._to_timestamp(end)
        if start:
            params['start'] = self._to_timestamp(start, base=end)
        return self._get(
            uri='api/v1/labels',
            params= params
        )


    def _get(self, uri, params, method='GET'):
        url = urljoin(self.endpoint, uri)
        assert method == 'GET'

        result = requests.get(
            url=url,
            params=params, auth=(self.username, self.password), verify=False
        ) #OK for auth to be None?
        return result.json()
