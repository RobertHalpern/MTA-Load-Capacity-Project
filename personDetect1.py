import cv2
import time
import torch
import numpy as np

# Assuming you have yolov8's PyTorch model loaded as 'model'
#def load_model():
#    model_path = '/Users/Rm501_09/Documents/MTA_ASR_24/yolov8s.pt'  # Update this path
#    model = torch.load(model_path)
#    model.eval()
#    return model
#

def load_model(model_path='/Users/Rm501_09/Documents/MTA_ASR_24/yolov8s.pt'):
    # Ensure the model_path is correct and points to the downloaded .pt file
    model = torch.load(model_path, map_location=torch.device('cpu'))
    model.eval()
    return model

model = load_model()

def capture_frame():
    ret, frame = cap.read()
    if ret:
        filename = f"frame_{int(time.time())}.png"
        cv2.imwrite(filename, frame)
        return filename
    return None

def detect_people_in_frame(frame_path):
    # Load image
    img = cv2.imread(frame_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.transpose(img, (2, 0, 1))
    img = torch.tensor(img, dtype=torch.float32)
    img /= 255.0  # Normalize to [0, 1]
    img = img.unsqueeze(0)  # Add batch dimension
    
    results = model(img)  # Adjust depending on the model's expected input
    
    # Process results (this will vary based on how your model outputs detections)
    print("Detected people count:", len(results))

cap = cv2.VideoCapture(0)

try:
    start_time = time.time()
    while True:
        if time.time() - start_time > 30:
            frame_path = capture_frame()
            if frame_path:
                detect_people_in_frame(frame_path)
            start_time = time.time()
finally:
    cap.release()
    cv2.destroyAllWindows()
