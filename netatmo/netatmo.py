from __future__ import annotations

import sys
from typing import TypedDict, cast

import requests

HEADERS = {"Content-Type": "application/x-www-form-urlencoded", "charset": "UTF-8"}


class OAuthResponse(TypedDict):
    access_token: str
    refresh_token: str
    scope: list[str]
    expires_in: int
    expire_in: int


class OAuthErrorResponse(TypedDict):
    error: str


class StationData(TypedDict):
    body: Body
    status: str
    time_exec: float
    time_server: int


class Body(TypedDict):
    devices: list[Device]
    user: User


class Device(TypedDict):
    _id: str
    station_name: str
    date_setup: int
    last_setup: int
    type: str
    last_status_store: int
    module_name: str
    firmware: int
    last_upgrade: int
    wifi_status: int
    reachable: bool
    co2_calibrating: bool
    data_type: list[str]
    place: Place
    home_id: str
    home_name: str
    dashboard_data: DashboardData
    modules: list[Module]


class Place(TypedDict):
    altitude: int
    city: str
    country: str
    timezone: str
    location: list[float]


class DashboardData(TypedDict):
    time_utc: int
    Temperature: float
    CO2: int
    Humidity: int
    Noise: int
    Pressure: int
    AbsolutePressure: float
    min_temp: float
    max_temp: float
    date_max_temp: int
    date_min_temp: int
    temp_trend: str
    pressure_trend: str


class Module(TypedDict):
    _id: str
    type: str
    module_name: str
    last_setup: int
    data_type: list[str]
    battery_percent: int
    reachable: bool
    firmware: int
    last_message: int
    last_seen: int
    rf_status: int
    battery_vp: int


class User(TypedDict):
    mail: str
    administrative: Administrative


class Administrative(TypedDict):
    lang: str
    reg_locale: str
    unit: int
    windunit: int
    pressureunit: int
    feel_like_algo: int


def get_oauth_token(
    chilent_id: str, client_secret: str, username: str, password: str
) -> str:
    url = "https://api.netatmo.com/oauth2/token"
    data = {
        "grant_type": "password",
        "client_id": chilent_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "scope": "read_station",
    }

    res = requests.post(url=url, headers=HEADERS, data=data)

    if "error" in res.json():
        print(cast(OAuthErrorResponse, res.json())["error"])
        sys.exit(1)

    access_token = cast(OAuthResponse, res.json())["access_token"]

    return access_token


def get_station_data(access_token: str) -> StationData:
    url = "https://api.netatmo.com/api/getstationsdata"
    data = {"access_token": access_token}

    res = requests.post(url=url, headers=HEADERS, data=data)

    return cast(StationData, res.json())
