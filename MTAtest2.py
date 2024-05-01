import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
import datetime
import re

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



# Part 2: Mapping the camera to the MTA API
# We're going to pretend that the personDetect2 script outputs both A) The number of people and B) the number of people in the frame. 


# Pulling the detected # of people from personDetect2.py 

# Path to the log file
log_file_path = 'app.log'

# Regular expression pattern to match lines with 'x persons'
person_pattern = re.compile(r'(\d+)\s+persons')

# Regular expression to extract the camera name from the file path
camera_name_pattern = re.compile(r'/Users/Rm501_09/Documents/MTA_ASR_24/video/(.+)\.webp')

# Function to search for 'x persons' and camera names in the log file
def search_persons_and_camera_in_log(file_path):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            # Search for number of persons
            person_match = person_pattern.search(line)
            # Search for camera name
            camera_match = camera_name_pattern.search(line)
            if person_match and camera_match:
                # Extracts the camera name from the match
                camera_name = camera_match.group(1)
                # Append both the number of persons and the camera name to results
                results.append((person_match.group(0), camera_name))
    return results

# Execute the function and print the results
detected_info = search_persons_and_camera_in_log(log_file_path)
for persons, camera_name in detected_info:
    print(f"Camera: {camera_name}, Detected: {persons}")
