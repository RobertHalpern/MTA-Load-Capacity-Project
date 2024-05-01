import logging
from ultralytics import YOLO
import torch
import numpy as np
import pandas

# Setup logging configuration
logging.basicConfig(level=logging.INFO, filename='model_results.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def read_camera_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def run_yolo_model(camera_name):
    source_path = f'/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/1/{camera_name}.jpg'
    model = YOLO("yolov8n.pt")
    results = model.predict(source=source_path, show=False, save=True, project='/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/results')
    return results

def log_results(camera_name, results):
    person_class_id = 0  # Adjust this based on your model's configuration
    # Iterate through the boxes
    person_count = 0
    for box in results[0].boxes:
        if box.cls == person_class_id:
            person_count += 1

    logging.info(f"{camera_name} - Number of people detected: {person_count}")



def process_cameras(camera_names):
    for camera_name in camera_names:
        results = run_yolo_model(camera_name)
        log_results(camera_name, results)

def main():
    camera_names = read_camera_names('consist.txt')
    process_cameras(camera_names)

if __name__ == '__main__':
    main()
