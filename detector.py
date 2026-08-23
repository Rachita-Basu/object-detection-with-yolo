import cv2
import pandas as pd
import numpy as np
from PIL import Image
from ultralytics import YOLO
import streamlit as st
import time

@st.cache_resource
def load_yolo_model(model_name: str):
    """
    Loads the YOLO model and caches it using Streamlit's cache_resource
    to avoid reloading the model weights on every rerun.
    """
    return YOLO(model_name)


class YoloDetector:
    def __init__(self, model_name: str = "yolov8n.pt"):
        """
        Initializes the YOLO Detector with a specific pre-trained model.
        Model options: 'yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', etc.
        """
        self.model_name = model_name
        self.model = load_yolo_model(model_name)
        # Class names map: id -> string
        self.class_names = self.model.names

    def detect(self, image: Image.Image, conf_threshold: float = 0.25, iou_threshold: float = 0.45, selected_classes: list = None):
        """
        Runs object detection on a PIL Image and returns the annotated image
        along with a Pandas DataFrame containing details about each detection.
        """
        # Convert PIL image to OpenCV format (BGR) for YOLO and annotation
        open_cv_image = np.array(image)
        # Handle grayscale or RGBA images
        if len(open_cv_image.shape) == 2:
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_GRAY2BGR)
        elif open_cv_image.shape[2] == 4:
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGBA2BGR)
        else:
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # Run inference
        results = self.model(
            open_cv_image, 
            conf=conf_threshold, 
            iou=iou_threshold, 
            verbose=False
        )

        detections = []
        annotated_image = open_cv_image.copy()

        # Check if results are returned
        if results and len(results) > 0:
            result = results[0]
            boxes = result.boxes
            
            for box in boxes:
                # Class id and label
                class_id = int(box.cls[0].item())
                label = self.class_names[class_id]
                
                # If target classes are specified, filter out unwanted classes
                if selected_classes and label not in selected_classes:
                    continue
                    
                confidence = float(box.conf[0].item())
                
                # Bounding box coordinates: [x_min, y_min, x_max, y_max]
                coords = box.xyxy[0].tolist()
                x_min, y_min, x_max, y_max = map(int, coords)
                
                # Store detection details for Pandas DataFrame
                detections.append({
                    "class_name": label,
                    "confidence": confidence,
                    "x_min": x_min,
                    "y_min": y_min,
                    "x_max": x_max,
                    "y_max": y_max
                })
                
                # Generate unique color based on class ID
                color = self.get_class_color(class_id)
                
                # Draw bounding box on the image
                cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), color, 2)
                
                # Draw text background and text
                text = f"{label} {confidence:.2f}"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(
                    annotated_image, 
                    (x_min, y_min - text_height - 5), 
                    (x_min + text_width, y_min), 
                    color, 
                    -1
                )
                cv2.putText(
                    annotated_image, 
                    text, 
                    (x_min, y_min - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (255, 255, 255), 
                    1, 
                    cv2.LINE_AA
                )

        # Convert back from BGR to RGB for Streamlit/PIL display
        annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        df_detections = pd.DataFrame(detections)
        
        # Ensure we return a DataFrame with expected columns even if empty
        if df_detections.empty:
            df_detections = pd.DataFrame(columns=["class_name", "confidence", "x_min", "y_min", "x_max", "y_max"])
            
        return Image.fromarray(annotated_image_rgb), df_detections

    def get_class_color(self, class_id: int):
        """
        Generates a consistent, visually pleasing BGR color for bounding boxes
        based on the class identifier.
        """
        # Seed pseudo-random generator with class_id to get consistent color
        np.random.seed(class_id + 5)
        color = np.random.randint(50, 255, size=3).tolist()
        return tuple(color)
