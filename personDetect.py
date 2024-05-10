import logging
from ultralytics import YOLO  # Ensure this import matches the actual YOLOv8 import

# Setup logging configuration
logging.basicConfig(level=logging.INFO, filename='model_results.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def read_camera_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def run_yolo_model(camera_name, index):
    # Specify the source image path
    source_path = f'/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/1/{camera_name}.jpg'
    # Load the YOLO model
    model = YOLO("yolov8n.pt")
    # Run prediction, setting the output to start from 'predict1'
    folder_name = f"predict{index + 1}"  # Naming folders starting from 'predict1'
    results = model.predict(source=source_path, show=False, save=True, project='/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/results', name=folder_name)
    return results

def log_results(camera_name, results):
    person_class_id = 0  # Adjust based on your model's class ID for persons
    person_count = 0
    # Count the number of persons detected
    for box in results[0].boxes:
        if box.cls == person_class_id:
            person_count += 1
    # Log the detection count
    logging.info(f"{camera_name} - Detected: {person_count} persons")

def process_cameras(camera_names):
    for index, camera_name in enumerate(camera_names):
        results = run_yolo_model(camera_name, index)
        log_results(camera_name, results)

def main():
    camera_names = read_camera_names('consist.txt')
    process_cameras(camera_names)

if __name__ == '__main__':
    main()
