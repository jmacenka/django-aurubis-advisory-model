# This file contains the OSIPIConnector class which is used to connect to the OSI PI system and retrieve data.
# Created by Jan Macenka @ 25 Sept 2023

# Library imports
import yaml
import requests
import pytz
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from requests.auth import HTTPBasicAuth

# Configuration imports
from config import (
    TIMEZONE,
    CHARGE_START_HOUR,
    CACHE_STORAGE_DURATION_HOURS,
    OSI_PI_PARAMETERS_REQUESTED,
    OSI_PI_WEBID_MAPPING,
)

class OSIPIConnector:
    """
    A class for connecting to an OSI PI system and retrieving data.

    Args:
        base_url (str): The base URL of the OSI PI system.
        username (str): The username for authentication.
        password (str): The password for authentication.
        timezone (str, optional): The timezone of the OSI PI system. Defaults to 'Europe/Berlin'.
        request_timeout_seconds (int, optional): The timeout for requests to the OSI PI system in seconds. Defaults to 120.

    Methods:
        get_data(start_time: datetime = None, end_time: datetime = None, verify_cert: bool = False) -> pd.DataFrame: Retrieves data from OSI PI system for a given time range, uses a local cache to minimize the number of web-requests to OSI-PI API.

    Internal Methods:
        _convert_timestamps(timestamp: datetime) -> str: Convert a timestamp to the correct format for the OSI PI system.
        _generate_batch_start_timestamp(charge_hour_start: int = CHARGE_START_HOUR) -> datetime: Generate a timestamp for the start of the current charge.
        _batch_retriev_data(start_time: datetime, end_time: datetime, verify_cert: bool = False, object_names: list = OSI_PI_PARAMETERS_REQUESTED) -> pd.DataFrame: Retrieve multiple data-ranges for same timespan and returns a Pandas DataFrame.

    Attributes:
        base_url (str): The base URL of the OSI PI system.
        auth (requests.auth.HTTPBasicAuth): The authentication object for requests to the OSI PI system.
        timezone (pytz.timezone): The timezone of the OSI PI system.
        request_timeout_seconds (int): The timeout for requests to the OSI PI system in seconds.
        webid_mapping (dict): A mapping of object names to their corresponding WebIDs.
        cached_data (pd.DataFrame): A Pandas DataFrame containing cached data from the OSI PI system.
    """
    def __init__(self, base_url: str, username: str, password: str, timezone: str = TIMEZONE, request_timeout_seconds: int = 120):

        # Check that base_url, username and password are provided
        if not base_url or base_url == '':
            raise ValueError("base_url must be provided")
        if not username or username == '':
            raise ValueError("username must be provided")
        if not password or password == '':
            raise ValueError("password must be provided")

        # Remove trailing slash from base_url if it exists
        if base_url.endswith('/'):
            base_url = base_url.rstrip('/')
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username.encode('utf-8'), password.encode('utf-8'))
        self.timezone = pytz.timezone(TIMEZONE)
        self.request_timeout_seconds = request_timeout_seconds
        self.webid_mapping = OSI_PI_WEBID_MAPPING

        # On instantiation, the current time is set as the start_timestamp
        start_timestamp = datetime.now(self.timezone)
        end_timestamp = self._generate_batch_start_timestamp()
        self.cached_data = self._batch_retriev_data(
            start_time=start_timestamp, 
            end_time = end_timestamp,
        )

    def _convert_timestamps(self, timestamp: datetime) -> str:
        """
        Convert a timestamp to the correct format for the OSI PI system.
        OSI-PI syntax is * equals now, *-1h equals one hour ago, *-1d equals one day ago, etc.
        """
        # If the timestamp is naive, assume it is in the timezone of the OSI PI system
        if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
            timestamp = timestamp.replace(tzinfo=self.timezone)

        # Calculate the difference in hours
        now = datetime.now(self.timezone)
        difference_in_hours = int((now - timestamp).total_seconds() / 3600)

        return f'*-{difference_in_hours}h'

    def _generate_batch_start_timestamp(self, charge_hour_start: int = CHARGE_START_HOUR) -> datetime:
        """
        Generate a timestamp for the start of the current charge which is set to (yesterday, h=CHARGE_START_HOUR).
        """
        timestamp = datetime.now(self.timezone)
        timestamp = timestamp - timedelta(days=1)
        timestamp = timestamp.replace(hour=charge_hour_start, minute=0, second=0, microsecond=0)
        return timestamp

    def _batch_retriev_data(self, start_time: datetime, end_time: datetime, verify_cert: bool = False) -> pd.DataFrame:
        """
        Retrieve multiple data-ranges for same timespan and returns a Pandas DataFrame.
        """
        # Create timestamps
        start_time_converted = self._convert_timestamps(start_time)
        end_time_converted = self._convert_timestamps(end_time)

        # Generate a list of tuples for the params of the request. the WebID field will have multiple values.
        params = [(('webid', self.webid_mapping.get(object_name, None))) for object_name in OSI_PI_PARAMETERS_REQUESTED]
        params.append(('startTime', start_time_converted,)) 
        params.append(('endTime', end_time_converted,))

        # Construct and validate the URL
        url = f"{self.base_url}/piwebapi/streamsets/recorded"

        # Fetch data from API
        response = requests.get(url, params=params, auth=self.auth, verify=verify_cert, timeout = self.request_timeout_seconds)
        if response.status_code == 200:
            response_object = response.json()

            # Unpack the response into a dict and convert into pandas DataFrame
            response_dict = {item.get('Name', None): {pd.Timestamp(entry.get('Timestamp',None)) : entry.get('Value',None) for entry in item.get('Items', [])} for item in response_object.get('Items', [])}

            # Convert into Pandas DataFrame
            df_request = pd.DataFrame(response_dict)
            df_request.index = pd.to_datetime(df_request.index)
            df_request.index = df_request.index.tz_convert(TIMEZONE)
            return df_request
        else:
            return pd.DataFrame() # Return empty DataFrame if nothing was returned

    def get_data(self, start_time: datetime = None, end_time: datetime = None, verify_cert: bool = False) -> pd.DataFrame:
        """
        Retrieves data from OSI PI system for a given time range.

        Args:
            start_time (datetime): Start time of the time range. If not provided, the default start time is generated.
            end_time (datetime): End time of the time range. If not provided, the current time is used.
            verify_cert (bool): Whether to verify the SSL certificate of the PI server.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the requested data.
        """

        # Make the start_time and end_time timezone aware
        if start_time is not None and start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=self.timezone)
        if end_time is not None and end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=self.timezone)

        # Check if cache is initialized and fetch minimum and maximum timestamps
        cache_has_data = False
        if self.cached_data is not None and not self.cached_data.empty:
            cache_timestamp_min = self.cached_data.index.min().to_pydatetime()
            cache_timestamp_max = self.cached_data.index.max().to_pydatetime()
            cache_has_data = True

        # If cache has no data, initialize it with the current time
        if not cache_has_data:
            self.cached_data = self._batch_retriev_data(
                start_time=start_time, 
                end_time = end_time,
                verify_cert=verify_cert,
            )
            df_response = self.cached_data
        
        # Fetch data that is not yet in the cache and merge it into the cache
        elif cache_has_data:
            # If older datat is requested than is in the cache, fetch it
            if start_time < cache_timestamp_min:
                self.cached_data = pd.concat([
                    self._batch_retriev_data(
                        start_time=start_time, 
                        end_time = cache_timestamp_min,
                        verify_cert=verify_cert,
                    ),
                    self.cached_data,
                ]).sort_index()

            # Fetch the latest data from last entry in the cache till the end_time
            if end_time > cache_timestamp_max:
                self.cached_data = pd.concat([
                    self.cached_data,
                    self._batch_retriev_data(
                        start_time=cache_timestamp_max, 
                        end_time = end_time,
                        verify_cert=verify_cert,
                    ),
                ]).sort_index()

            df_response = self.cached_data[(self.cached_data.index >= start_time) & (self.cached_data.index <= end_time)]

            # Clear the cache if it is older than CACHE_STORAGE_DURATION_HOURS
            cache_cut_off_timestamp = datetime.now(self.timezone) - timedelta(hours=CACHE_STORAGE_DURATION_HOURS)
            self.cached_data = self.cached_data[self.cached_data.index >= cache_cut_off_timestamp]
        
        return df_response