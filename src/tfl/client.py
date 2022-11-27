'''
Client.py
'''
from typing import Dict
import os
import sys
import requests
#import pandas as pd
from tfl.exceptions import TFLAPIException, TFLRequestException

#Add abs path for intellisense
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))




class Client():
    '''
    Client
    '''
    def __init__(self) -> None:
        self.test = 'test'
        self.api_url = 'https://api.tfl.gov.uk/'
        self.session = self._init_session()
        self.request_timeout = 1000

    def _get_headers(self) -> Dict:
        headers = {
            'Accept': 'application/json',
        }
        return headers

    def _init_session(self) -> requests.Session:
        headers = self._get_headers()
        session = requests.session()
        session.headers.update(headers)
        return session

    def _request(self, method, uri: str, signed: bool, **kwargs):
        print(kwargs)
        # set default requests timeout
        kwargs['timeout'] = self.request_timeout
        if signed:
            pass

        response = getattr(self.session, method)(uri, params = kwargs)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: requests.Response):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not 200 <= response.status_code < 300:
            raise TFLAPIException(response, response.status_code, response.text)
        try:
            return response.json()
        except ValueError as exc:
            raise TFLRequestException(f'Invalid Response: {response.text}') from exc

    def _create_api_uri(self, path: str, signed: bool = True) -> str:
        url = self.api_url
        if signed:
            pass
        return url + '/' + path

    def _request_api(self, method, path: str, signed: bool = False, **kwargs):
        uri = self._create_api_uri(path, signed)
        return self._request(method, uri, signed, **kwargs)

    def _get(self, path, signed=False, **kwargs):
        return self._request_api('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs) -> Dict:
        return self._request_api('post', path, signed, **kwargs)

    def _put(self, path, signed=False,  **kwargs) -> Dict:
        return self._request_api('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs) -> Dict:
        return self._request_api('delete', path, signed, **kwargs)

    def get_line_ids(self) -> Dict:
        '''Get line ids'''
        return self._get('Line/Route', False, serviceTypes = 'Night')

    def get_valid_modes(self):
        '''Get valid modes'''
        return self._get('Line/Meta/Modes', False)

    def get_routes(self, mode):
        '''Get routes'''
        return self._get(f'Line/Mode/{mode}/Route')


if __name__=="__main__":
    data = Client().get_routes('tube')
    for i in data:
        for key, value in i.items():
            print(f'{key}:{value}')
