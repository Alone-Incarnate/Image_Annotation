import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLOv8 model
yolo_model = YOLO("yolov8n.pt")

# Function to draw bounding boxes and labels on the original image
def annotate_image(original_image, detections):
    annotated_image = original_image.copy()  # Create a copy to annotate
    for detection in detections:
        x1, y1, x2, y2 = map(int, detection.xyxy)  # Get bounding box coordinates
        class_id = int(detection.cls)  # Get class index
        class_name = yolo_model.names[class_id]  # Get class name

        # Draw the bounding box
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

        # Put the label above the bounding box
        cv2.putText(annotated_image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return annotated_image

# Load an image
image_path = "Your_iamge_path.jpg"
image = cv2.imread(image_path)

# Perform object detection
results = yolo_model(image)
detections = results.xyxy[0]  # Assuming results are returned in this format

# Annotate the image
annotated_image = annotate_image(image, detections)

# Display the annotated image
cv2.imshow("Annotated Image", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
