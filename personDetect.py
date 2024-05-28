import logging
from ultralytics import YOLO  # Ensure this import matches the actual YOLOv8 import
import os

# Setup logging configuration
logging.basicConfig(level=logging.INFO, filename='model_results.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def read_camera_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def run_yolo_model(camera_name, folder_num):
    """Runs the YOLO model on images in specified folders."""
    # Specify the source image path dynamically
    source_path = f'/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/{folder_num}/{camera_name}.jpg'
    
    # Check if the source image exists
    if not os.path.exists(source_path):
        print(f"Source path {source_path} does not exist. Skipping...")
        return None

    # Load the YOLO model
    model = YOLO("yolov8n.pt")
    
    # Naming folders starting from 'predict1' to 'predict22'
    folder_name = f"predict{folder_num}"
    
    # Ensure the project directory exists
    project_dir = f'/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/results/{folder_name}'
    os.makedirs(project_dir, exist_ok=True)
    
    # Run prediction and save results in the appropriate folder
    results = model.predict(source=source_path, show=False, save=True, project=project_dir, name=folder_name)
    
    print(f"Results saved in {project_dir}")
    return results

def log_results(camera_name, folder_num, results):
    person_class_id = 0  # Adjust based on your model's class ID for persons
    person_count = 0
    # Count the number of persons detected
    for box in results[0].boxes:
        if box.cls == person_class_id:
            person_count += 1
    # Log the detection count
    logging.info(f"{camera_name}, predict{folder_num}, Detected: {person_count} persons")

def process_cameras(camera_names):
    for camera_name in camera_names:
        for folder_num in range(1, 23):
            results = run_yolo_model(camera_name, folder_num)
            if results is not None:
                log_results(camera_name, folder_num, results)

def main():
    camera_names = read_camera_names('consist.txt')
    process_cameras(camera_names)

if __name__ == '__main__':
    main()
