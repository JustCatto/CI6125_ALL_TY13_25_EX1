import http
import math
import os
import time

import requests
import dotenv
from requests import HTTPError

dotenv.load_dotenv()
APP_ID = "Unified API"
API_KEY = os.getenv("API_KEY")


def get_bus_times(stop_code: str, bus_num:str,ttd: int):
    url = f"https://api.tfl.gov.uk/StopPoint/{stop_code}/arrivals"
    requesting = True
    delay = 1
    response = ""
    while requesting:

        try:
            response = requests.get(
                url,
                params={
                    "app_id":APP_ID,
                    "app_key":API_KEY
                }
            )
            response.raise_for_status()
            requesting = False
        except HTTPError as e:
            if e.response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
                time.sleep(delay)
                delay = delay * 2
            else:
                raise e
    buses = []
    seenMatching = False
    for entry in response.json():
        if entry["lineId"] == bus_num:
            seenMatching = True
            if int(entry["timeToStation"]) > ttd:
                buses.append(str(math.ceil(int(entry["timeToStation"])/60)))
    if seenMatching == False:
        return "No matching buses found on live timetable"

    if len(buses) < 1:
        return "You will not make any buses on the live timetable."

    times = " and ".join(buses)
    return f"You will make the {bus_num} busses that arrive in {times} minutes:"


print(get_bus_times("490006412E2","57", 420))