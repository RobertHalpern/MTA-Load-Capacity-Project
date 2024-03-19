import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
import datetime

def load_stops(static_gtfs_path):
    stops_df = pd.read_csv(f"{static_gtfs_path}/stops.txt", usecols=['stop_id', 'stop_name'])
    # Create a mapping for stop IDs to names for quick lookup
    stop_id_to_name = {row['stop_id']: row['stop_name'] for index, row in stops_df.iterrows()}
    return stop_id_to_name

def fetch_realtime_data(api_key):
    feed_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l'
    headers = {'x-api-key': api_key}
    response = requests.get(feed_url, headers=headers)
    return response.content if response.status_code == 200 else None

def display_train_positions(api_key, static_gtfs_path):
    stop_id_to_name = load_stops(static_gtfs_path)
    feed_content = fetch_realtime_data(api_key)
    if feed_content:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(feed_content)
        current_time = int(datetime.datetime.now().timestamp())

        unique_trains = {}  # Track unique trains to avoid duplicates

        for entity in feed.entity:
            if entity.HasField('trip_update'):
                for update in entity.trip_update.stop_time_update:
                    # Assuming updates are near-term; adjust time window as needed
                    if update.arrival.time >= current_time and update.arrival.time <= current_time + 900:
                        trip_id = entity.trip_update.trip.trip_id
                        stop_id = update.stop_id
                        stop_name = stop_id_to_name.get(stop_id.strip("NS"), "Unknown")
                        direction = "North" if "N" in stop_id else "South" if "S" in stop_id else "Terminus"
                        if trip_id not in unique_trains:
                            print(f"Trip ID: {trip_id}, Next Stop: {stop_name}, Direction: {direction}, Arrival Time: {datetime.datetime.fromtimestamp(update.arrival.time).strftime('%Y-%m-%d %H:%M:%S')}")
                            unique_trains[trip_id] = True

api_key = "prFGb6l4Ugx0iK5LaOCc67RLHRXd6o84BZx0bkTj"  # Replace with your actual MTA API key
static_gtfs_path = "/Users/Rm501_09/Documents/MTA_ASR_24/google_transit_supplemented/"
display_train_positions(api_key, static_gtfs_path)
