"""
Python client for the Kaiterra REST API.
"""

import json
import aiohttp
from typing import List
from enum import Enum
from kaiterra_async_client import dateutil


class AQIStandard(Enum):
    """
    Denotes a scale according to which air quality index should be calculated
    from pollutant readings.
    """
    USA = 'us'
    China = 'cn'
    India = 'in'


class Units(Enum):
    """
    Lists units in which sensor-reported values may be reported.  Use .value
    to return the short string representation of these enums.
    """
    Unknown = '?'
    Count = 'x'
    Percent = '%'
    DegreesCelsius = 'C'
    DegreesFahrenheit = 'F'
    MilligramsPerCubicMeter = 'mg/m³'
    MicrogramsPerCubicMeter = 'µg/m³'
    PartsPerMillion = 'ppm'
    PartsPerBillion = 'ppb'

    @staticmethod
    def from_str(s: str):
        for v in Units.__members__.values():
            if v.value == s:
                return v
        raise ValueError("'{}' isn't a known value for Units".format(s))


class KaiterraAPIClient(object):
    """
    KaiterraAPIClient connects to the Kaiterra API over HTTP.

    :param base_url: URL under which the API can be found.  The default value is sufficient
    for most cases.
    :param api_key: Secret key, obtained from the Kaiterra dashboard at
    https://dashboard.kaiterra.cn, that uniquely identifies the client making the request.
    :param hmac_secret: Secret key that can be used to authorize requests without
    transmitting the key over the wire.  (Note: most clients don't use this)
    :param aqi_standard: Indicates that air quality index (AQI) should be calculated
    for reported polluants where applicable, according to the standard set by the
    US EPA, Chinese MEP, or other given governing body.  The index returned is the Kaiterra
    Overall Index described at https://support.kaiterra.com/hc/en-us/articles/360016529993-What-is-the-Overall-Index-
    :param preferred_units: List of Units preferred by the client.  For instance,
    passing [Units.DegreesFahrenheit] will cause all temperature quantities to be reported
    in degrees Fahrenheit instead of the default, which is degrees Celsius.
    """

    def __init__(self,
                 session,
                 base_url='https://api.kaiterra.cn',
                 api_key=None,
                 hmac_secret=None,
                 aqi_standard=None,
                 preferred_units=None
                 ):
        """Constructs a new KaiterraAPIClient object."""
        self._base_url = base_url.rstrip('/')
        self._api_key = api_key
        self._hmac_secret = hmac_secret
        self._preferred_units = []
        self._aqi_standard = aqi_standard
        self._session = session

        if preferred_units is not None:
            for u in preferred_units:
                self._preferred_units.append(u)

        if self._api_key is None and self._hmac_secret is None:
            raise ValueError("Must specify one of api_key or hmac_secret")

        if self._api_key is not None and self._hmac_secret is not None:
            raise ValueError("Must specify only one of api_key or hmac_secret")

    async def get_latest_sensor_readings(self, sensor_ids: List[str]) -> List[dict]:
        """
        Retrieves the latest sensor readings for the given sensors.

        :param sensor_ids: A list of sensor IDs whose data to return.  IDs must look like
        /lasereggs/00000000-0001-0001-0000-00007e57c0de for Laser Eggs, or
        /sensedges/00000000-0031-0001-0000-00007e57c0de for Sensedges.  The maximum
        length of this list is 100.
        :returns: a list of dictionaries containing sensor data, where the list has
        one element corresponding to each ID passed in sensor_ids.  Sensors that don't exist
        or have never reported any data will have values of None.  Otherwise, each dictionary's
        keys are the names of the measurement parameters ('pm25', 'pm10', 'humidity', etc.)
        and the values are themselves dictionaries with the following keys:

        - units: a Units enum showing the units in which the quantity is being reported
        - source: (optional) for Sensedges, this is the model of the sensor that captured
        the reading; e.g. 'km100', 'km102'
        - points: a list of one or more data points -- dictionaries -- with the following keys:
            - ts: a datetime object that is the time at which the quantity was measured
            - value: the numeric value of the reading
            - aqi: (optional) the air quality index of the reading, if applicable
        """
        from urllib.parse import urlencode

        if isinstance(sensor_ids, str):
            raise ValueError("sensor_ids must be a list of strings")

        if len(sensor_ids) > 100:
            raise ValueError("sensor_ids is too long; max length is 100")

        requests = []

        get_params = ['format=series_major']
        if self._aqi_standard is not None:
            get_params.append('aqi=' + self._aqi_standard.value)
        for u in self._preferred_units:
            get_params.append('units=' + u.value)

        for sid in sensor_ids:
            if not self._is_valid_sensor_id(sid):
                raise ValueError('sensor ID ' + sid + ' is invalid')
            req = {
                'method': 'GET',
                'relative_url': sid + "?" + '&'.join(get_params),
            }
            requests.append(req)

        r = await self._do_request(
            '/v1/batch',
            headers={'Content-Type': 'application/json'},
            json=requests)

        # Do some slight reformatting and parse dates
        return [self._parse_series_major_single_points(x) for x in r]

    def _parse_series_major_single_points(self, response: dict) -> dict:
        import collections
        if not isinstance(response, collections.Mapping):
            return None
        if response.get('code', 0) < 200 or response.get('code', 0) >= 400:
            return None

        body = json.loads(response['body'])
        params = body.get('latest', None)
        if not params:
            params = body.get('info.aqi', None)
            if not params:
                return None

        parsed = {}
        for param in params:
            if len(param['points']) == 0:
                continue

            points = param['points']
            point = points[0]
            point['ts'] = dateutil.parse_rfc3339(point['ts'])
            new_pt = {
                'units': Units.from_str(param['units']),
            }
            if 'source' in param:
                new_pt['source'] = param['source']
            new_pt['points'] = [point]

            parsed[param['param']] = new_pt

        return parsed

    async def _do_request(self, relative_url, *, params=None, headers=None, json=None):
        """
        Executes an HTTP GET/POST against the given resource.  The request is authorized
        using the credentials given to __init__.
        """
        params = params or {}
        headers = headers or {}
        if 'key' in params:
            raise ValueError("don't pass the 'key' parameter to individual requests; authorization is already handled by KaiterraAPIClient")

        if self._api_key:
            params['key'] = self._api_key

        url = self._base_url + '/' + relative_url.lstrip('/')
        async with self._session.post(url, params=params, headers=headers, json=json, raise_for_status=True) as r:
            return await r.json()

    def _is_valid_sensor_id(self, sid: str) -> bool:
        """
        Ensures the given ID is a valid sensor ID.
        """
        import re

        m = re.match(r'/?(lasereggs?|sensedges?)/([0-9a-f]{32}|[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})', sid.lower())
        if not m:
            return False

        return True
