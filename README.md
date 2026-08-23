# 🔍 Object Detection using a YOLO Detector

> 🎓 **Final Year Project**
> 
> This repository contains my Final Year Project: a real-time object detection, classification, and visual analytics application developed using a YOLO detector, Python, Pandas, and Streamlit.

---

## 🚀 Key Features

*   **2D Image Detection**: Upload custom images or run the detector on default street scenes to analyze bounding boxes and confidence scores.
*   **Real-Time Video Inference**: Process video uploads frame-by-frame and visualize object count trends over time.
*   **Live Webcam stream (Local only)**: Connect your local camera feed to run inference at high frames-per-second (FPS) with automated resource release.
*   **Pandas-Powered Analytics Dashboard**: Gather detection counts, class occurrence statistics, and export all logged events to a CSV file.
*   **Model Selection**: Switch between YOLOv8 weights (Nano, Small, Medium) and filter specific classes dynamically from the UI.

---

## 🛠️ Setup and Installation

### 1. Prerequisites
Ensure you have **Python 3.9 - 3.12** installed on your system.

### 2. Run the App Locally

1.  Open your terminal and navigate to the project directory:
    ```bash
    cd "Object detection with YOLO"
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
3.  Activate the virtual environment:
    *   **Windows (PowerShell)**: `.\.venv\Scripts\Activate.ps1`
    *   **Windows (CMD)**: `.\.venv\Scripts\activate.bat`
    *   **macOS/Linux**: `source .venv/bin/activate`
4.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
5.  Launch the application:
    ```bash
    streamlit run app.py
    ```

---

## 📦 Tech Stack
*   **Language**: Python
*   **Deep Learning Framework**: Ultralytics YOLOv8 (PyTorch backend)
*   **Data Analysis & Log Storage**: Pandas
*   **User Interface**: Streamlit
*   **Charts & Visualizations**: Plotly
*   **Image & Video Handlers**: OpenCV, Pillow
