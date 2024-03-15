import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
import time

def load_stops(static_gtfs_path):
    stops_df = pd.read_csv(f"{static_gtfs_path}/stops.txt", usecols=['stop_id', 'stop_name'])
    # Some stops may have suffixes N/S in real-time but not in static data.
    stop_id_to_name = {stop_id.split('N')[0].split('S')[0]: stop_name for stop_id, stop_name in zip(stops_df['stop_id'], stops_df['stop_name'])}
    return stop_id_to_name

def get_direction(stop_id):
    if "N" in stop_id:
        return "North"
    elif "S" in stop_id:
        return "South"
    else:
        return "Terminus"

def fetch_and_display_realtime_data(api_key, stop_id_to_name):
    feed_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l'
    headers = {'x-api-key': api_key}
    response = requests.get(feed_url, headers=headers)
    current_time = int(time.time())

    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                for update in entity.trip_update.stop_time_update:
                    # Filter out stop_time_updates that are too far in the future
                    if update.arrival.time >= current_time - 60*5 and update.arrival.time <= current_time + 60*15:
                        stop_id = update.stop_id
                        direction = get_direction(stop_id)
                        # Attempt to strip directional suffix for matching
                        base_stop_id = stop_id.strip("NS")
                        stop_name = stop_id_to_name.get(base_stop_id, "Unknown Stop")
                        print(f"Stop Name: {stop_name}, Direction: {direction}, Arrival Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(update.arrival.time))}")
    else:
        print("Failed to fetch GTFS-RT data.")

api_key = "prFGb6l4Ugx0iK5LaOCc67RLHRXd6o84BZx0bkTj"  # Replace with your actual MTA API key
static_gtfs_path = "/Users/Rm501_09/Documents/MTA_ASR_24/google_transit_supplemented/"
stop_id_to_name = load_stops(static_gtfs_path)
fetch_and_display_realtime_data(api_key, stop_id_to_name)
