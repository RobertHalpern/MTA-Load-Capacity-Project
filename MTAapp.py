import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
import datetime
import re
from privatekey import MTA_API_KEY

def load_stops(static_gtfs_path):
    stops_df = pd.read_csv(f"{static_gtfs_path}/stops.txt", usecols=['stop_id', 'stop_name'])
    # Create a mapping for stop IDs to names for quick lookup
    stop_id_to_name = {row['stop_id']: row['stop_name'] for index, row in stops_df.iterrows()}
    return stop_id_to_name

def fetch_realtime_data(api_key):
    feed_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l'
    headers = {'x-api-key': MTA_API_KEY}
    response = requests.get(feed_url, headers=headers)
    return response.content if response.status_code == 200 else None

def display_train_positions(api_key, static_gtfs_path, output_file):
    stop_id_to_name = load_stops(static_gtfs_path)
    feed_content = fetch_realtime_data(api_key)
    if feed_content:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(feed_content)
        current_time = int(datetime.datetime.now().timestamp())

        unique_trains = {}  # Track unique trains to avoid duplicates

        with open(output_file, 'a') as file:  # Append mode to continue writing to the same file
            print(f"\nSchedules", file=file)
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
                                print(f"Trip ID: {trip_id}, Stop ID: {stop_id}, Next Stop: {stop_name}, Direction: {direction}, Arrival Time: {datetime.datetime.fromtimestamp(update.arrival.time).strftime('%Y-%m-%d %H:%M:%S')}", file=file)
                                unique_trains[trip_id] = True

# Path to the log file
log_file_path = 'model_results.log'

# Regular expression pattern to match lines with 'x persons'
person_pattern = re.compile(r'(\d+)\s+persons')

# Regular expression to extract the camera name and folder number from the log
camera_pattern = re.compile(r'camera(\d+)')
folder_pattern = re.compile(r'predict(\d+)')

def search_persons_and_camera_in_log(file_path):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            # Extract camera number, folder number, and persons count
            camera_match = camera_pattern.search(line)
            folder_match = folder_pattern.search(line)
            person_match = person_pattern.search(line)
            
            if camera_match and folder_match and person_match:
                camera_num = camera_match.group(1)
                folder_num = folder_match.group(1)
                person_count = person_match.group(1)
                results.append((camera_num, folder_num, person_count))
                
    return results

# Execute the function and print the results
detected_info = search_persons_and_camera_in_log(log_file_path)

# Define output file
output_file = 'output.txt'

# Open the file 'output.txt' in write mode ('w') for initial write
with open(output_file, 'w') as file:
    print(f"Source Camera, Folder Number, Detected Count", file=file)
    for camera_num, folder_num, persons in detected_info:
        print(f"{camera_num}, {folder_num}, {persons}", file=file)

# Call the function to display train positions and append to the same file
static_gtfs_path = "/Users/Rm501_09/Documents/MTA_ASR_24/google_transit_supplemented/"
display_train_positions(MTA_API_KEY, static_gtfs_path, output_file)
