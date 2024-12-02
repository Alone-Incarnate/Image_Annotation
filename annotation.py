import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO
from PIL import Image

# Load the YOLOv8 model
yolo_model = YOLO("yolov8n.pt")

# Function to draw bounding boxes and labels on the original image
def annotate_image(original_image, detections):
    annotated_image = original_image.copy()  # Create a copy to annotate
    for detection in detections:
        # Extract bounding box coordinates
        x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy().astype(int)  # Convert tensor to numpy and then to int
        class_id = int(detection.cls.cpu().numpy())  # Convert tensor to numpy and then to int
        class_name = yolo_model.names[class_id]  # Get class name

        # Draw the bounding box
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

        # Put the label above the bounding box
        cv2.putText(annotated_image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return annotated_image

# Streamlit UI
st.title("Image Annotation")
st.write("Upload an image to Annotate.")

# Image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Perform object detection
    results = yolo_model.predict(image)  # Use predict() method to get results
    detections = results[0].boxes  # Access the boxes from the first result

    # Annotate the image
    annotated_image = annotate_image(image, detections)

    # Convert annotated image to RGB for display
    annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

    # Display the annotated image
    st.image(annotated_image_rgb, caption="Annotated Image", use_column_width=True)
