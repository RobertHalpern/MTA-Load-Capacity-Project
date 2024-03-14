import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
import datetime
import pytz

def get_current_time():
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    est_now = utc_now.astimezone(pytz.timezone("America/New_York"))
    print(f"Current Time (EST): {est_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current Time (UTC): {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")

stops_file_path = '/Users/Rm501_09/Documents/MTA_ASR_24/google_transit_supplemented/stops.txt'
stops_df = pd.read_csv(stops_file_path, usecols=['stop_id', 'stop_name'])
stops_mapping = dict(zip(stops_df['stop_id'], stops_df['stop_name']))

def get_stop_name(stop_id):
    return stops_mapping.get(stop_id, "Unknown Stop")

api_key = "prFGb6l4Ugx0iK5LaOCc67RLHRXd6o84BZx0bkTj"
feed_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l'

headers = {'x-api-key': api_key}

response = requests.get(feed_url, headers=headers, allow_redirects=True)

get_current_time()

if response.status_code == 200:
    print("Successfully accessed the MTA Realtime API!")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    for entity in feed.entity[:5]:
        print(f"\nEntity ID: {entity.id}")
        stop_ids = [update.stop_id for update in entity.trip_update.stop_time_update]
        if 'L29' in stop_ids:
            direction_name = "Canarsie-Rockaway Pkwy"
        elif 'L01' in stop_ids:
            direction_name = "8 Av"
        else:
            direction_name = "Unknown direction"
        print(f"Direction: {direction_name}")

        for update in entity.trip_update.stop_time_update:
            stop_id = update.stop_id
            stop_name = get_stop_name(stop_id)
            print(f"Stop ID: {stop_id}, Stop Name: {stop_name}")
else:
    print(f"Failed to access the MTA Realtime API. Status code: {response.status_code}")