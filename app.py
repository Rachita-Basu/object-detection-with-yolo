import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import time
import requests
import io
import cv2
import tempfile
import plotly.express as px
import plotly.graph_objects as go

from detector import YoloDetector

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="YOLOv8 Object Detection & Real-time Analytics Suite",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Custom Fonts and Title Gradients */
    .title-text {
        font-family: 'Outfit', 'Inter', sans-serif;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F8F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        font-family: 'Inter', sans-serif;
        color: #888888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card design */
    .metric-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #2e324a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #ff4b4b;
    }
    
    /* Status classes */
    .success-badge {
        background-color: rgba(46, 204, 113, 0.15);
        color: #2ecc71;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Define Sample Media URLs
SAMPLE_IMAGE_URL = "https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/assets/bus.jpg"
SAMPLE_VIDEO_URL = "https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/assets/shuttle.mp4"

# Cache function to download sample image
@st.cache_data(show_spinner=False)
def download_sample_image(url):
    try:
        response = requests.get(url, timeout=10)
        return Image.open(io.BytesIO(response.content))
    except Exception as e:
        st.error(f"Error downloading sample image: {e}")
        return None

# Initialize Session State for Analytics Log across pages
if "analytics_log" not in st.session_state:
    st.session_state["analytics_log"] = pd.DataFrame(
        columns=["timestamp", "source", "class_name", "confidence", "x_min", "y_min", "x_max", "y_max"]
    )

# Sidebar Configuration
st.sidebar.markdown("<h2 style='text-align: center;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)

# 1. Model Selection
model_size = st.sidebar.selectbox(
    "Choose YOLO Model Size",
    ["Nano (Fastest, ~12MB)", "Small (Balanced, ~22MB)", "Medium (Accurate, ~50MB)"],
    index=0,
    help="Nano is ideal for CPU/real-time speed. Medium is slower but more accurate."
)

model_map = {
    "Nano (Fastest, ~12MB)": "yolov8n.pt",
    "Small (Balanced, ~22MB)": "yolov8s.pt",
    "Medium (Accurate, ~50MB)": "yolov8m.pt"
}
selected_model_name = model_map[model_size]

# Show loader for Model Initialization
with st.sidebar.status("Loading Model Weights...", expanded=True) as status:
    st.write(f"Fetching {selected_model_name} weights...")
    try:
        detector = YoloDetector(selected_model_name)
        status.update(label="Model Loaded Successfully!", state="complete", expanded=False)
    except Exception as e:
        status.update(label="Error Loading Model", state="error", expanded=True)
        st.error(str(e))
        st.stop()

# 2. Advanced Parameters
st.sidebar.markdown("### 🎚️ Threshold Parameters")
conf_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.25,
    step=0.05,
    help="Minimum confidence level required to register a detection."
)

iou_threshold = st.sidebar.slider(
    "IoU Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.45,
    step=0.05,
    help="Intersection over Union (IoU) threshold for Non-Maximum Suppression (controls overlapping boxes)."
)

# 3. Class Filtering
all_classes = sorted(list(detector.class_names.values()))
select_all = st.sidebar.checkbox("Select All Classes", value=True)

if select_all:
    selected_classes = all_classes
else:
    selected_classes = st.sidebar.multiselect(
        "Target Classes",
        all_classes,
        default=["person", "car", "bicycle", "dog", "cat"]
    )

# Clear Session Data
if st.sidebar.button("🗑️ Clear Analytics Logs", use_container_width=True):
    st.session_state["analytics_log"] = pd.DataFrame(
        columns=["timestamp", "source", "class_name", "confidence", "x_min", "y_min", "x_max", "y_max"]
    )
    st.sidebar.success("Session logs cleared!")

# About Section
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎓 About Project")
st.sidebar.markdown(
    "**Object Detection using YOLO** is a Final Year Project. It implements real-time 2D object detection, classification, and visual analytics."
    "\n\n**Live Link:** [streamlit.app](https://object-detection-with-yolo-project.streamlit.app/)"
)

# Main Title Header
st.markdown("<div class='title-text'>🔍 YOLOv8 Detection & Analytics Suite</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>A powerful real-time deep learning computer vision dashboard with Pandas-driven insights.</div>", unsafe_allow_html=True)

# Tabs Configuration
tab_image, tab_video, tab_webcam, tab_analytics = st.tabs([
    "🖼️ Image Detection", 
    "🎥 Video Processing", 
    "📹 Live Webcam",
    "📊 Analytics Dashboard"
])

# --- TAB 1: IMAGE DETECTION ---
with tab_image:
    st.header("Static Image Detection")
    st.write("Upload an image file or run the detector on our pre-loaded sample image.")
    
    col_input, col_config = st.columns([2, 1])
    
    with col_input:
        image_source = st.radio("Choose Image Input Source", ["Use Sample Image", "Upload Custom Image"], horizontal=True)
        uploaded_image = None
        
        if image_source == "Upload Custom Image":
            uploaded_image_file = st.file_uploader("Drag and drop your image here", type=["jpg", "jpeg", "png"])
            if uploaded_image_file:
                uploaded_image = Image.open(uploaded_image_file)
        else:
            with st.spinner("Downloading sample image..."):
                uploaded_image = download_sample_image(SAMPLE_IMAGE_URL)
                
    with col_config:
        st.info("💡 Adjust thresholds and target classes in the sidebar to dynamically filter detections on the fly!")
    
    if uploaded_image:
        st.subheader("Inference & Visualizations")
        
        # Display side-by-side
        col_orig, col_annot = st.columns(2)
        
        with col_orig:
            st.image(uploaded_image, caption="Original Image", use_container_width=True)
            
        with col_annot:
            start_time = time.time()
            # Run detection
            annotated_img, df_dets = detector.detect(
                uploaded_image, 
                conf_threshold=conf_threshold, 
                iou_threshold=iou_threshold, 
                selected_classes=selected_classes
            )
            latency = (time.time() - start_time) * 1000 # ms
            
            st.image(annotated_img, caption="Annotated Result (YOLOv8)", use_container_width=True)
            
        # Logging detections in Streamlit session state
        if not df_dets.empty:
            # Prepare rows to log
            log_rows = df_dets.copy()
            log_rows["timestamp"] = pd.Timestamp.now()
            log_rows["source"] = "Image Upload"
            st.session_state["analytics_log"] = pd.concat([st.session_state["analytics_log"], log_rows], ignore_index=True)
            
        # Metrics Display
        st.subheader("📊 Statistics & Logs")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Objects Detected", len(df_dets))
        with col_m2:
            st.metric("Inference Latency", f"{latency:.1f} ms")
        with col_m3:
            avg_conf = df_dets["confidence"].mean() if not df_dets.empty else 0.0
            st.metric("Average Confidence", f"{avg_conf:.2%}")
            
        # Detections Pandas DataFrame Table
        if not df_dets.empty:
            st.dataframe(df_dets, use_container_width=True)
            
            # Export CSV
            csv_data = df_dets.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Detection CSV",
                data=csv_data,
                file_name="detections_image.csv",
                mime="text/csv",
                key="download_image_csv"
            )
        else:
            st.warning("No objects matching your selected classes were detected above the confidence threshold.")

# --- TAB 2: VIDEO PROCESSING ---
with tab_video:
    st.header("Real-Time Video Detection")
    st.write("Upload a video to analyze it frame-by-frame and visualize dynamic detection trends.")
    
    video_source = st.radio("Choose Video Input Source", ["Use Sample Video", "Upload Custom Video"], horizontal=True)
    uploaded_video_path = None
    
    if video_source == "Upload Custom Video":
        uploaded_video_file = st.file_uploader("Upload video file", type=["mp4", "avi", "mov"])
        if uploaded_video_file:
            # Create a temporary file to save the uploaded video
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_file.write(uploaded_video_file.read())
            uploaded_video_path = temp_file.name
            temp_file.close()
    else:
        # Cache-download sample video locally
        sample_vid_path = "sample_shuttle.mp4"
        if not os.path.exists(sample_vid_path):
            with st.spinner("Downloading sample video shuttle.mp4..."):
                try:
                    r = requests.get(SAMPLE_VIDEO_URL, timeout=30)
                    with open(sample_vid_path, "wb") as f:
                        f.write(r.content)
                    uploaded_video_path = sample_vid_path
                except Exception as e:
                    st.error(f"Error downloading sample video: {e}")
        else:
            uploaded_video_path = sample_vid_path

    if uploaded_video_path:
        # Action button to trigger video processing
        if st.button("🚀 Process Video & Run Inference", type="primary"):
            cap = cv2.VideoCapture(uploaded_video_path)
            
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Setup side by side live stream and dynamic chart
            col_video_display, col_realtime_chart = st.columns([1, 1])
            
            with col_video_display:
                st.subheader("Annotated Video Stream")
                frame_placeholder = st.empty()
                
            with col_realtime_chart:
                st.subheader("Detections Count Over Time")
                chart_placeholder = st.empty()
                
            # Keep track of counts over time for plotting
            frame_count_data = []
            frame_index = 0
            
            # Temporary list to log results during this run
            video_log_rows = []
            
            start_proc_time = time.time()
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert OpenCV BGR to Pillow RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                
                # Run YOLO Detection
                annotated_img, df_dets = detector.detect(
                    pil_img,
                    conf_threshold=conf_threshold,
                    iou_threshold=iou_threshold,
                    selected_classes=selected_classes
                )
                
                # Render current annotated frame
                frame_placeholder.image(annotated_img, channels="RGB", use_container_width=True)
                
                # Log stats
                current_time = pd.Timestamp.now()
                for _, row in df_dets.iterrows():
                    video_log_rows.append({
                        "timestamp": current_time,
                        "source": "Video Stream",
                        "class_name": row["class_name"],
                        "confidence": row["confidence"],
                        "x_min": int(row["x_min"]),
                        "y_min": int(row["y_min"]),
                        "x_max": int(row["x_max"]),
                        "y_max": int(row["y_max"])
                    })
                
                # Record details for plot
                total_detected = len(df_dets)
                frame_count_data.append({"Frame": frame_index, "Detections": total_detected})
                
                # Render live time series graph
                df_counts = pd.DataFrame(frame_count_data)
                fig = px.line(
                    df_counts, 
                    x="Frame", 
                    y="Detections", 
                    title="Real-Time Detection Count",
                    labels={"Detections": "Number of Objects", "Frame": "Frame Index"}
                )
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff'
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                
                # Update progress bar
                frame_index += 1
                progress = min(frame_index / total_frames, 1.0)
                progress_bar.progress(progress)
                status_text.text(f"Processing frame {frame_index}/{total_frames} ({progress * 100:.1f}%)")
                
            cap.release()
            total_duration = time.time() - start_proc_time
            
            # Clean up temp file
            if video_source == "Upload Custom Video" and os.path.exists(uploaded_video_path):
                try:
                    os.remove(uploaded_video_path)
                except Exception:
                    pass
            
            # Write final status
            status_text.success(f"Processing Complete in {total_duration:.1f} seconds! (Average: {total_duration/frame_index*1000:.1f} ms per frame)")
            
            # Log results to overall session log
            if video_log_rows:
                df_video_log = pd.DataFrame(video_log_rows)
                st.session_state["analytics_log"] = pd.concat([st.session_state["analytics_log"], df_video_log], ignore_index=True)
                
                st.subheader("Detections Summary")
                st.dataframe(df_video_log.head(100), use_container_width=True)
                
                csv_vid = df_video_log.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Video Detection CSV",
                    data=csv_vid,
                    file_name="detections_video.csv",
                    mime="text/csv",
                    key="download_video_csv"
                )

# --- TAB 3: LIVE WEBCAM STREAM ---
with tab_webcam:
    st.header("📹 Live Webcam Stream Detection")
    st.write("Run real-time object detection using your system's primary web camera feed.")
    
    col_w_ctrl, col_w_help = st.columns([1, 2])
    with col_w_ctrl:
        camera_index = st.number_input("Camera Device Index", min_value=0, max_value=10, value=0, step=1, help="Index of the camera device (0 is typically the built-in webcam).")
        run_webcam = st.toggle("🔌 Activate Live Webcam Feed", value=False)
    with col_w_help:
        st.info("💡 Make sure to grant your browser access to your camera if prompted. When you toggle this off, the camera device will be released automatically.")
        
    if run_webcam:
        # Open webcam feed
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            st.error(f"Could not open webcam device at index {camera_index}. Please check connection or try a different device index.")
            st.info("ℹ️ **Deployment Note**: If this application is hosted in the cloud (e.g., Streamlit Community Cloud), webcam capture using OpenCV is not supported because cloud servers do not have local camera hardware. To use live webcam mode, please clone and run the application locally on your machine.")
        else:
            frame_placeholder = st.empty()
            webcam_metrics_placeholder = st.empty()
            
            # Keep a session list for current webcam run
            webcam_log_rows = []
            frame_idx = 0
            
            fps_avg = 0.0
            
            try:
                while run_webcam:
                    start_time = time.time()
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Error reading frame from webcam.")
                        break
                    
                    # Convert OpenCV BGR to Pillow RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(frame_rgb)
                    
                    # Run YOLO Inference
                    annotated_img, df_dets = detector.detect(
                        pil_img,
                        conf_threshold=conf_threshold,
                        iou_threshold=iou_threshold,
                        selected_classes=selected_classes
                    )
                    
                    # Compute inference FPS
                    latency = (time.time() - start_time)
                    fps_val = 1.0 / latency if latency > 0 else 0.0
                    fps_avg = (fps_avg * 0.9) + (fps_val * 0.1) if frame_idx > 0 else fps_val
                    
                    # Render current annotated frame
                    frame_placeholder.image(annotated_img, channels="RGB", use_container_width=True)
                    
                    # Log detections
                    current_time = pd.Timestamp.now()
                    for _, row in df_dets.iterrows():
                        webcam_log_rows.append({
                            "timestamp": current_time,
                            "source": "Live Webcam",
                            "class_name": row["class_name"],
                            "confidence": row["confidence"],
                            "x_min": int(row["x_min"]),
                            "y_min": int(row["y_min"]),
                            "x_max": int(row["x_max"]),
                            "y_max": int(row["y_max"])
                        })
                    
                    # Render live stats
                    webcam_metrics_placeholder.markdown(f"""
                    **Live FPS:** `{fps_avg:.1f}` | **Current Objects Detected:** `{len(df_dets)}`
                    """)
                    
                    frame_idx += 1
                    # Small sleep to allow streamlit to process other threads
                    time.sleep(0.01)
                    
            finally:
                cap.release()
                
            # Log results to overall session log if any
            if webcam_log_rows:
                df_webcam_log = pd.DataFrame(webcam_log_rows)
                st.session_state["analytics_log"] = pd.concat([st.session_state["analytics_log"], df_webcam_log], ignore_index=True)
                st.success(f"Webcam session stopped. Logged {len(webcam_log_rows)} detections to analytics!")

# --- TAB 4: ANALYTICS DASHBOARD ---
with tab_analytics:
    st.header("📊 Session Analytics Dashboard")
    st.write("Examine aggregated statistics, distributions, and insights from all detections run in this session.")
    
    df_logs = st.session_state["analytics_log"]
    
    if df_logs.empty:
        st.info("No data captured yet. Run detections on the Image, Video, or Webcam tabs to generate session logs.")
    else:
        # Top-level metrics
        total_records = len(df_logs)
        unique_classes = df_logs["class_name"].nunique()
        avg_confidence = df_logs["confidence"].mean()
        
        col_met1, col_met2, col_met3 = st.columns(3)
        with col_met1:
            st.markdown(f"""
            <div class='metric-card'>
                <h4>Total Detections Logged</h4>
                <h2 style='color:#ff4b4b;'>{total_records}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_met2:
            st.markdown(f"""
            <div class='metric-card'>
                <h4>Unique Class Categories</h4>
                <h2 style='color:#3498db;'>{unique_classes}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_met3:
            st.markdown(f"""
            <div class='metric-card'>
                <h4>Average Detection Confidence</h4>
                <h2 style='color:#2ecc71;'>{avg_confidence:.1%}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        
        # Visualizations
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("Object Counts by Class")
            class_counts = df_logs["class_name"].value_counts().reset_index()
            class_counts.columns = ["Class", "Count"]
            
            fig_bar = px.bar(
                class_counts, 
                x="Class", 
                y="Count", 
                color="Count",
                color_continuous_scale="reds",
                title="Total Occurrences per Object Class"
            )
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_c2:
            st.subheader("Confidence Distribution by Class")
            fig_box = px.box(
                df_logs, 
                x="class_name", 
                y="confidence", 
                color="class_name",
                title="Confidence Levels Spread per Object Class",
                labels={"class_name": "Class Name", "confidence": "Confidence Score"}
            )
            fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
            st.plotly_chart(fig_box, use_container_width=True)
            
        st.write("---")
        
        # Timeline distribution
        st.subheader("Detections Timeline (Chronological Log)")
        st.dataframe(df_logs.sort_values(by="timestamp", ascending=False), use_container_width=True)
        
        # Download all data
        csv_all = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Session Log (CSV)",
            data=csv_all,
            file_name="yolo_session_analytics.csv",
            mime="text/csv",
            key="download_all_csv"
        )
