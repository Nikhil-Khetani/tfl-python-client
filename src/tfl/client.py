'''
Client.py
'''
from typing import Dict
import requests
#import pandas as pd

from tfl.exceptions import TFLAPIException, TFLRequestException

class BaseClient():
    '''
    BaseClient object to store headers and initiate API calls from

    Parameters
    ----------
    api_url : str (default: 'https://api.tfl.gov.uk/')
        The root url from which all endpoints can be accessed.

    See Also
    --------
    Client : BaseClient object with functions for calling the TFL Unified API

    Notes
    -----
    

    Examples
    --------
    '''
    def __init__(self, api_url = 'https://api.tfl.gov.uk/') -> None:
        self.test = 'test'
        self.api_url = api_url
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

class Client(BaseClient):
    '''
    Client object to store headers and initiate API calls from

    Parameters
    ----------
    api_url : str (default: 'https://api.tfl.gov.uk/')
        The root url from which all endpoints can be accessed.

    See Also
    --------
    BaseClient : Base class for API calls.

    Notes
    -----

    Examples
    --------
    '''
    def __init__(self, api_url='https://api.tfl.gov.uk/') -> None:
        super().__init__(api_url = api_url)

    def get_valid_modes(self):
        '''
        Get valid modes
        Gets a list of valid modes
        '''
        return self._get('Line/Meta/Modes', False)

    def get_routes(self, mode):
        '''
        Get routes
        Gets all lines and their valid routes for given modes,
        including the name and id of the originating and terminating
        stops for each route
        '''
        return self._get(f'Line/Mode/{mode}/Route')

    def get_line_ids(self, service_type = 'Regular') -> Dict:
        """
        Get line ids.

        Parameters
        ----------
        service_type : str (default: 'Regular')
            Specify serviceTypes, either 'Regular' or 'Night'

        Returns
        -------
        Dict
            Output of API request.

        Notes
        -----

        See Also
        --------
        """
        if service_type not in ['Regular','Night']:
            raise Exception('Invalid serviceTypes argument')
        return self._get('Line/Route', False, serviceTypes = service_type)


if __name__=="__main__":
    data = Client().get_routes('tube')
    for i in data:
        for key, value in i.items():
            print(f'{key}:{value}')
