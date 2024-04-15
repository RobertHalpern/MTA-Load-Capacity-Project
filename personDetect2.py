import sys
import logging

# Setup logging configuration
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

# Replace stdout with logging
sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO)

# Example usage
print("This will be logged to both console and file.")


from ultralytics import YOLO
import string, torch, numpy

model = YOLO("yolov8n.pt")  # load a pretrained YOLOv8n model 
results = model.predict(source='/Users/Rm501_09/Documents/MTA_ASR_24/video/image2.webp', show=False, save=False, project='/Users/Rm501_09/Documents/MTA_ASR_24/video/results') 



# def __len__(self):  # override len(results)
#     """Return the length of the data tensor."""
#     return len(self.data)
# def __init__(self, orig_img, path, names, boxes=None, masks=None, probs=None, keypoints=None, obb=None) -> None:
#     self._keys = "boxes", "masks", "probs", "keypoints", "obb"
# def __len__(self):
#         """Return the number of detections in the Results object."""
#         for k in self._keys:
#             v = getattr(self, k)
#             if v is not None:
#                 return len(v)
            
# print(len(results)) # this just prints 1, it's not right



"""
import subprocess

command = 'python3 personDetect2.py' # ... it's just recursing

# Open + write file
with open('/Users/Rm501_09/Documents/MTA_ASR_24/video/output.txt', 'w') as file:
    # Run the command and redirect the output to the file
    subprocess.run(command, shell=True, stdout=file, stderr=subprocess.STDOUT)

"""

# print(results)


# Process results list
# for results in results:
#    boxes = results.boxes  # Boxes object for bounding box outputs
#    masks = results.masks  # Masks object for segmentation masks outputs
#    keypoints = results.keypoints  # Keypoints object for pose outputs
#    probs = results.probs  # Probs object for classification outputs
#    results.show()  # display to screen
#    results.save(filename='result.jpg')  # save to disk
# print("KEYPOINTS:", keypoints)
# print("BOXES:", boxes)
# print("MASKS:", masks)
# print("PROBS:", probs)
# x = keypoints.count()
# print("number of spaces:", x)

# model.train(data="coco128.yaml", epochs=epochs)  # train the model
# model.val()  # evaluate model performance on the validation set
# model.export(format="onnx")  # export the model to ONNX format
# result = model('/Users/Rm501_09/Documents/MTA_ASR_24/video/image.webp', save = True, project = "'/Users/Rm501_09/Documents/MTA_ASR_24/video/results/")

# print(result, "is the answer!!!!!!!!!") # Currently need to make sure it knows what to predict. Rn it likely counts ALL predictions.
# print(type(result))
# """
# """
# import supervision as sv

# detections = sv.Detections.from_ultralytics(result)
# detections = detections[detections.class_id == classes.index("class name")]
# print(len(detections))


# def count_objects(predictions, target_classes):
#     object_counts = {x: 0 for x in target_classes}
#     for prediction in predictions:
#         for c in prediction.boxes.cls:
#             c = int(c)
#             if c in target_classes:
#                 object_counts[c] += 1
#             elif c not in target_classes:
#                 object_counts[c] = 1

#     present_objects = object_counts.copy()

#     for i in object_counts:
#         if object_counts[i] < 1:
#             present_objects.pop(i)

#     return present_objects

# """
