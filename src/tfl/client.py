'''
Client.py
'''
from typing import Dict, List
import requests
import json
#import pandas as pd
import logging
import sys
from tfl.exceptions import TFLAPIException, TFLRequestException

class BaseClient():
    """
    BaseClient object to store headers and initiate API calls from

    Parameters
    ----------
    api_url : str, default: 'https://api.tfl.gov.uk/'
        The root url from which all endpoints can be accessed.

    Returns
    -------

    See Also
    --------
    Client : BaseClient object with functions for calling the TFL Unified API

    Notes
    -----

    Examples
    --------

    Raises
    ------
    TFLAPIException
        _description_
    TFLRequestException
        _description_
    """
    def __init__(self, api_url = 'https://api.tfl.gov.uk/') -> None:
        self.test = 'test'
        self.api_url = api_url
        self.session = self._init_session()
        self.request_timeout = 1000

    def _get_headers(self) -> Dict:
        """
        Generated headers for http request

        Returns
        -------
        Dict
            Headers for http request
        """
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
        # print(response.status_code)
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

    def get(self, path, signed=False, **kwargs):
        return self._request_api('get', path, signed, **kwargs)

    def post(self, path, signed=False, **kwargs) -> Dict:
        return self._request_api('post', path, signed, **kwargs)

    def put(self, path, signed=False,  **kwargs) -> Dict:
        return self._request_api('put', path, signed, **kwargs)

    def delete(self, path, signed=False, **kwargs) -> Dict:
        return self._request_api('delete', path, signed, **kwargs)

class Client(BaseClient):
    """
    Client object to store headers and initiate API calls from.

    Parameters
    ----------
    api_url : str, default: 'https://api.tfl.gov.uk/'
        The root url from which all endpoints can be accessed.

    See Also
    --------
    BaseClient : Base class for API calls.

    Notes
    -----

    Examples
    --------
    """
    def __init__(self, api_url='https://api.tfl.gov.uk/') -> None:
        super().__init__(api_url = api_url)
        self.line = LineEndpoint(self)

    # def get_valid_modes(self):
    #     """
    #     _summary_

    #     Returns
    #     -------
    #     _type_
    #         _description_
    #     """
    #     return self._get('Line/Meta/Modes', False)

    # def get_routes(self, mode):
    #     """
    #     Gets all lines and their valid routes for given modes,
    #     including the name and id of the originating and terminating
    #     stops for each route

    #     Parameters
    #     ----------
    #     mode : str
    #         _description_

    #     Returns
    #     -------
    #     Dict
    #         _description_
    #     """
    #     return self._get(f'Line/Mode/{mode}/Route')

    # def get_line_ids(self, service_type = 'Regular') -> Dict:
    #     """
    #     Get line ids.

    #     Parameters
    #     ----------
    #     service_type : str, default: 'Regular'
    #         Specify serviceTypes, either 'Regular' or 'Night'

    #     Returns
    #     -------
    #     Dict
    #         Output of API request.

    #     Notes
    #     -----

    #     See Also
    #     --------
    #     """
    #     if service_type not in ['Regular','Night']:
    #         raise Exception('Invalid serviceTypes argument')
    #     return self._get('Line/Route', False, serviceTypes = service_type)


class LineEndpoint():
    """
    _summary_
    
    _extended_summary_

    Attributes
    ----------
    client: Client
        Client for https://api.tfl.gov.uk/
    """
    def __init__(self, client) -> None:
        self.client = client
    
    def get_valid_modes(self):
        """
        Gets a list of valid modes

        Returns
        -------
        _type_
            _description_

        Examples
        -------
        >>> self.get_valid_modes()
        [
            {
                "isTflService": true,
                "isFarePaying": true,
                "isScheduledService": true,
                "modeName": "string",
                "motType": "string",
                "network": "string"
            }
        ]
        """
        return self.client.get('Line/Meta/Modes')
    
    def get_severity_codes(self):
        """
        Gets a list of valid severity codes
                    
        Examples
        --------
        >>> self.get_severity_codes()
        [
            {
                "modeName": "string",
                "severityLevel": 0,
                "description": "string"
            }
        ]
        """
        return self.client.get('Line/Meta/Severity')

    def get_valid_disruption_categories(self):
        """
        Gets a list of valid disruption categories
                    
        Examples
        --------
        >>> self.get_valid_disruption_categories()
        [
        "string"
        ]
        """
        return self.client.get('Line/Meta/DisruptionCategories')

    def get_valid_service_types(self):
        """
        Gets a list of valid ServiceTypes to filter on
        
        Examples
        --------
        >>> self.get_valid_service_types()
        [
        "string"
        ]
        """
        return self.client.get('Line/Meta/ServiceTypes')

    def get_lines_by_ids(self, ids: List[str]):
        """
        Gets lines that match the specified line ids.
        
        Parameters
        ----------
        ids : List[str]
            A comma-separated list of line ids e.g. victoria,circle,N133. Max. approx. 20 ids.

        >>> self.get_lines_by_ids(['victoria','circle'])
        [
        {
            "id": "string",
            "name": "string",
            "modeName": "string",
            "disruptions": [
            {...
            }
            ],
            "created": "2023-12-25T15:49:28.801Z",
            "modified": "2023-12-25T15:49:28.801Z",
            "lineStatuses": [...],
            "routeSections": [...],
            "serviceTypes": [...],
            "crowding": {...}
        }
        ]
        """
        id_list = ','.join(ids)
        return self.client.get(f'Line/{id_list}')
    
    def get_lines_for_mode(self, modes: List[str]):
        """
        Gets lines that serve the given modes.
        
        Parameters
        ----------
        modes : List[str]
            A comma-separated list of modes e.g. tube,dlr
        
        Examples
        --------
        >>> self.get_lines_for_mode(['tube','dlr'])
        [
        {
            "id": "string",
            "name": "string",
            "modeName": "string",
            "disruptions": [
            {...
            }
            ],
            "created": "2023-12-25T15:49:28.801Z",
            "modified": "2023-12-25T15:49:28.801Z",
            "lineStatuses": [...],
            "routeSections": [...],
            "serviceTypes": [...],
            "crowding": {...}
        }
        ]"""
        mode_list = ','.join(modes)
        return self.client.get(f'Line/Mode/{mode_list}')
    
    def get_valid_routes_for_all_lines(self, service_types: List[str]=["Regular"]):
        """
        Get all valid routes for all lines, including the name and id of the originating and terminating stops for each route.

        Parameters
        ----------
        service_types : List[str], optional
            A comma seperated list of service types to filter on. Supported values: Regular, Night. By default ["Regular"].

        Examples
        --------
        >>> self.get_valid_routes_for_all_lines(service_types=['Regular','Night'])
        [
        {
            "id": "string",
            "name": "string",
            "modeName": "string",
            "disruptions": [
            {...
            }
            ],
            "created": "2023-12-25T15:49:28.801Z",
            "modified": "2023-12-25T15:49:28.801Z",
            "lineStatuses": [...],
            "routeSections": [...],
            "serviceTypes": [...],
            "crowding": {...}
        }
        ]"""
        return self.client.get("Line/Route", params=json.dumps({'serviceTypes':','.join(service_types)}))


    def get_valid_routes_for_line_ids(self, ids:List[str], service_types: List[str]=["Regular"]):
        """
        Get all valid routes for given line ids, including the name and id of the originating and terminating stops for each route.
        
        Parameters
        ----------
        ids : List[str]
            A comma-separated list of line ids e.g. victoria,circle,N133. Max. approx. 20 ids.
        service_types : List[str], optional
            A comma seperated list of service types to filter on. Supported values: Regular, Night. By default ["Regular"].
        
        Examples
        --------
        >>> self.get_valid_routes_for_line_ids(['victoria','circle'],service_types=['Regular','Night'])
        [
        {
            "id": "string",
            "name": "string",
            "modeName": "string",
            "disruptions": [
            {...
            }
            ],
            "created": "2023-12-25T15:49:28.801Z",
            "modified": "2023-12-25T15:49:28.801Z",
            "lineStatuses": [...],
            "routeSections": [...],
            "serviceTypes": [...],
            "crowding": {...}
        }
        ]"""
        id_list = ','.join(ids)
        return self.client.get(f'Line/{id_list}/Route', params=json.dumps({'ServiceTypes':','.join(service_types)}))


    def get_valid_routes_for_modes(self, modes:List[str], service_types: List[str]=["Regular"]):
        """
        Get all valid routes for given modes, including the name and id of the originating and terminating stops for each route.
        
        Parameters
        ----------
        modes : List[str]
            A comma-separated list of modes e.g. tube,dlr
        service_types : List[str], optional
            A comma seperated list of service types to filter on. Supported values: Regular, Night. By default ["Regular"].
        
        Examples
        --------
        >>> self.get_valid_routes_for_modes(['tube','dlr'],service_types=['Regular','Night'])
        [
        {
            "id": "string",
            "name": "string",
            "modeName": "string",
            "disruptions": [
            {...
            }
            ],
            "created": "2023-12-25T15:49:28.801Z",
            "modified": "2023-12-25T15:49:28.801Z",
            "lineStatuses": [...],
            "routeSections": [...],
            "serviceTypes": [...],
            "crowding": {...}
        }
        ]"""
        mode_list = ','.join(modes)
        return self.client.get(f'Line/Mode/{mode_list}/Route', params=json.dumps({'serviceTypes':','.join(service_types)}))

    def get_valid_routes_for_line_id(self, line_id:str, direction:str, service_types: List[str]=["Regular"], exclude_crowding: bool=False):
        """
        Gets all valid routes for given line id, including the sequence of stops on each route.
        
        Parameters
        ----------
        id : str
            A single line id e.g. victoria
        direction : str
            The direction of travel. Can be inbound or outbound.
        service_types : List[str], optional
            A comma seperated list of service types to filter on. Supported values: Regular, Night. By default ["Regular"].
        exclude_crowding : bool
            That excludes crowding from line disruptions. Can be true or false.
            
        Examples
        --------
        >>> self.get_valid_routes_for_line_id('victoria','inbound',service_types=['Regular','Night'])
        {
        "lineId": "string",
        "lineName": "string",
        "direction": "string",
        "isOutboundOnly": true,
        "mode": "string",
        "lineStrings": [
            "string"
        ],
        "stations": [...],
        "stopPointSequences": [...],
        "orderedLineRoutes": [...]
        }
        """
        return self.client.get(f'Line/{line_id}/Route/Sequence/{direction}', params=json.dumps({'serviceTypes':','.join(service_types), 'excludeCrowding':exclude_crowding}))
    
    def get_line_status_between_dates(self, ids: List[str], detail: bool, start_date: str, end_date: str):
        """
        Gets the line status for given line ids during the provided dates e.g Minor Delays

        Parameters
        ----------
        ids : List[str]
            A comma-separated list of line ids e.g. victoria,circle,N133. Max. approx. 20 ids.
        detail : bool
            Include details of the disruptions that are causing the line status including the affected stops and routes
        start_date : str
            Format YYYY-MM-DD
        end_date : str
            Format YYYY-MM-DD
        Examples
        --------
        >>> self.get_line_status_between_dates(['victoria', 'circle'],True,'2023-03-01','2023-03-07')
        [
        {
            "id": "string",
            "name": "string",
            "modeName": "string",
            "disruptions": [...],
            "created": "2023-12-25T15:49:28.801Z",
            "modified": "2023-12-25T15:49:28.801Z",
            "lineStatuses": [...],
            "routeSections": [...],
            "serviceTypes": [...],
            "crowding": {...}
        }
        ]
        """
        id_list = ','.join(ids)
        # return self.client.get(f"Line/{id_list}/Status/{start_date}/to/{end_date}", params=json.dumps({'detail':detail, 'dateRange.startDate':start_date,'dateRange.endDate':end_date}))
        return self.client.get(f"Line/{id_list}/Status/{start_date}/to/{end_date}", params={"detail":str(detail).lower()})

    def get_line_status(self, ids: List[str], detail: bool):
        """
        Gets the line status of for given line ids e.g Minor Delays
        
        Parameters
        ----------
        ids : List[str]
            A comma-separated list of line ids e.g. victoria,circle,N133. Max. approx. 20 ids.
        detail : bool
            Include details of the disruptions that are causing the line status including the affected stops and routes

        Examples
        --------
        >>> self.get_line_status(['victoria', 'circle],True)
        [
        {
            "id": "string",
            "name": "string",
            "modeName": "string",
            "disruptions": [...],
            "created": "2023-12-25T15:49:28.801Z",
            "modified": "2023-12-25T15:49:28.801Z",
            "lineStatuses": [...],
            "routeSections": [...],
            "serviceTypes": [...],
            "crowding": {...}
        }
        ]
        """
        id_list = ','.join(ids)
        return self.client.get(f"Line/{id_list}/Status", params={'detail':detail})

    def search_lines_or_routes(self, query: str, modes: List[str]|None=None, service_types: List[str]=["Regular"]):
        """
        Search for lines or routes matching the query string
                
        Parameters
        ----------
        query : str
            Search term e.g victoria
        modes : List[str]|None
            A comma-separated list of modes e.g. tube,dlr. Optional.
        service_types : List[str], optional
            A comma seperated list of service types to filter on. Supported values: Regular, Night. By default ["Regular"].
        
        Examples
        --------
        >>> self.search_lines_or_routes('query_str'):
        

        {
        "input": "string",
        "searchMatches": [
            {
            "lineId": "string",
            "mode": "string",
            "lineName": "string",
            "lineRouteSection": [...],
            "matchedRouteSections": [... ],
            "matchedStops": [
                {
                "routeId": 0,
                "parentId": "string",
                "stationId": "string",
                "icsId": "string",
                "topMostParentId": "string",
                "direction": "string",
                "towards": "string",
                "modes": [
                    "string"
                ],
                "stopType": "string",
                "stopLetter": "string",
                "zone": "string",
                "accessibilitySummary": "string",
                "hasDisruption": true,
                "lines": [...
                ],
                "status": true,
                "id": "string",
                "url": "string",
                "name": "string",
                "lat": 0,
                "lon": 0
                }
            ],
            "id": "string",
            "url": "string",
            "name": "string",
            "lat": 0,
            "lon": 0
            }
        ]
        }

        """
        if modes is not None:
            params = {'modes':modes,'serviceTypes':service_types}
        else:
            params = {'serviceTypes':service_types}

        return self.client.get(f"Line/Search/{query}", params=params)

    def get_line_status_by_severity(self, severity: int):
        """
        Gets the line status for all lines with a given severity.

        Parameters
        ----------
        severity : int
            The level of severity (eg: a number from 0 to 14)
        """
        if severity < 0 or severity > 14:
            raise ValueError("Severity must be between 0 and 14 inclusive")
        return self.client.get(f"Line/Status/{severity}")

    def get_line_status_by_mode(self, modes: List[str], detail : bool, severity: int|None = None):
        """
        Gets the line status for all lines for the given modes.
        
        Parameters
        ----------
        modes : List[str]
            A comma-separated list of modes to filter by. e.g. tube,dlr
        detail : bool
            Include details of the disruptions that are causing the line status including the affected stops and routes
        severity : int | None, optional
            If specified, ensures that only those line status(es) are returned within the lines that have disruptions with the matching severity level. By default None.
        """
        if severity is None:
            return self.client.get(f"Line/Mode/{','.join(modes)}/Status")
        else:
            return self.client.get(f"Line/Mode/{','.join(modes)}/Status", params={"severityLevel":severity}) 

    def get_stations(self, line_id: str, tfl_operated_national_rail_stations_only: bool = False):
        """
        Gets a list of the stations that serve the given line id
        
        Parameters
        ----------
        line_id : str
            A single line id e.g. victoria
        tfl_operated_national_rail_stations_only : bool, optional
            If the national-rail line is requested, this flag will filter the national rail stations so that only those operated by TfL are returned, by default False
        """
        return self.client.get(f"Line/{line_id}/StopPoints", params={"tflOperatedNationalRailStationsOnly": tfl_operated_national_rail_stations_only})

    def get_timetable_for_station(self, line_id:str, from_stop_point_id: str, to_stop_point_id: str|None = None):
        """
        Gets the timetable for a specified station on the given line with specified destination

        Parameters
        ----------
        line_id : str
            A single line id e.g. victoria
        from_stop_point_id : str
            The originating station's stop point id (station naptan code e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name)
        to_stop_point_id : str | None, optional
            The destination stations's Naptan code, by default None
        """
        if to_stop_point_id is None:
            return self.client.get(f"Line/{line_id}/Timetable/{from_stop_point_id}")
        else:
            return self.client.get(f"Line/{line_id}/Timetable/{from_stop_point_id}/to/{to_stop_point_id}")

    def get_disruptions_for_line_ids(self, ids: List[str]):
        """
        Get disruptions for the given line ids

        Parameters
        ----------
        ids : List[str]
            A comma-separated list of line ids e.g. victoria,circle,N133. Max. approx. 20 ids.
        """
        return self.client.get(f"Line/{','.join(ids)}/Disruption")

    def get_disruptions_for_modes(self, modes:List[str]):
        """
        Get disruptions for all lines of the given modes.

        Parameters
        ----------
        modes : List[str]
            A comma-separated list of modes e.g. tube,dlr
        """
        return self.client.get(f"Line/Mode/{','.join(modes)}/Disruption")

    def get_arrival_predictions(self, ids: List[str], stop_point_id: str, direction:str|None=None, destination_station_id:str|None=None):
        """
        Get the list of arrival predictions for given line ids based at the given stop
        
        Parameters
        ----------
        ids : List[str]
            A comma-separated list of line ids e.g. victoria,circle,N133. Max. approx. 20 ids.
        stop_point_id : str
            Id of stop to get arrival predictions for (station naptan code e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name).
        direction : str, optional
            Optional. The direction of travel. Can be inbound or outbound or all. If left blank, and destinationStopId is set, will default to all
        destination_stop_id : str, optional
            Optional. Id of destination stop
        """
        params = {}
        if direction is not None:
            params["direction"] = direction
        if destination_station_id is not None:
            params["destinationStationId"] = destination_station_id
        return self.client.get(f"Line/{','.join(ids)}/Arrivals/{stop_point_id}", params=params)

if __name__=="__main__":
    # data = Client().get_routes('tube')
    data = Client().line.get_valid_routes_for_all_lines()
    for i in data:
        for key, value in i.items():
            print(f'{key}:{value}')
