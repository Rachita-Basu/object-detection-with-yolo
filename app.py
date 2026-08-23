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
    page_title="Object Detection with YOLO - Made Clear",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (ClinicOCR-inspired UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Body Overrides */
    .stApp {
        background-color: #f8fafc !important; /* Slate-50 */
        color: #0f172a !important; /* Slate-900 */
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    /* Brand Header */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .brand-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #0f766e; /* Teal-700 */
        color: #ffffff;
        font-weight: bold;
        border-radius: 12px;
        width: 36px;
        height: 36px;
        font-size: 1.25rem;
        box-shadow: 0 4px 14px rgba(15, 118, 110, 0.2);
    }
    .brand-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.45rem;
        font-weight: bold;
        line-height: 1;
        color: #0f172a;
    }
    .brand-subtitle {
        font-size: 0.62rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: #0d9488; /* Teal-600 */
        margin-top: 1px;
    }

    /* Hero Editorial Heading */
    .hero-heading {
        font-family: 'DM Serif Display', serif;
        font-size: 3.8rem;
        font-weight: 500;
        line-height: 0.88;
        letter-spacing: -0.05em;
        color: #0f172a;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .hero-heading-teal {
        color: #0d9488; /* Teal-600 */
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #64748b; /* Slate-500 */
        margin-bottom: 2rem;
    }

    /* Clinic-style Cards */
    .clinic-card {
        background-color: #ffffff;
        border: 1px solid rgba(15, 118, 110, 0.08);
        border-radius: 1.6rem;
        padding: 1.8rem;
        box-shadow: 0 25px 70px rgba(12, 82, 83, 0.05);
        margin-bottom: 1.5rem;
    }

    /* Evidence Steps Metrics */
    .evidence-step {
        border: 1px solid rgba(15, 118, 110, 0.08);
        background-color: #ffffff;
        border-radius: 1.3rem;
        padding: 1.3rem;
        box-shadow: 0 15px 40px rgba(12, 82, 83, 0.03);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .evidence-step:hover {
        transform: translateY(-2px);
        box-shadow: 0 25px 50px rgba(12, 82, 83, 0.08);
    }
    .evidence-label {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        padding: 4px 10px;
        border-radius: 10px;
    }
    .label-cyan {
        background-color: #f0fdfa;
        color: #0f766e;
    }
    .label-amber {
        background-color: #fffbeb;
        color: #b45309;
    }
    .label-slate {
        background-color: #f8fafc;
        color: #475569;
    }

    /* Custom Input and Layout overrides */
    div.stButton > button {
        background-color: #0f766e !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 8px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.15) !important;
        transition: all 0.2s !important;
    }
    div.stButton > button:hover {
        background-color: #0d9488 !important;
        box-shadow: 0 6px 18px rgba(15, 118, 110, 0.25) !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Serve the landing experience before initializing the model-heavy workspace.
if "show_workspace" not in st.session_state:
    st.session_state["show_workspace"] = False

if not st.session_state["show_workspace"]:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="stAppViewContainer"] { background: #f5fbf8 !important; }
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 1040px !important;
            padding-top: 3.4rem !important;
            padding-bottom: 4.5rem !important;
        }
        .landing-nav {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 6rem; color: #102d32;
        }
        .landing-brand { display: flex; align-items: center; gap: 10px; }
        .landing-mark {
            position: relative; width: 31px; height: 31px; box-sizing: border-box;
            border: 2px solid #0f766e; border-right-color: transparent;
            border-bottom-color: transparent;
        }
        .landing-mark:after {
            content: ''; position: absolute; width: 7px; height: 7px; border-radius: 50%;
            top: 10px; left: 10px; background: #f4755c; box-shadow: 0 0 0 3px rgba(244,117,92,.12);
        }
        .landing-brand strong { display: block; font-size: 0.82rem; letter-spacing: .12em; }
        .landing-brand small { display: block; margin-top: 1px; color: #188076; font-size: .53rem; font-weight: 700; letter-spacing: .16em; }
        .landing-nav span { color: #597274; font-size: .75rem; font-weight: 600; }
        .landing-hero { max-width: 680px; margin: 0 auto; text-align: center; }
        .landing-kicker {
            display: inline-block; border: 1px solid rgba(15,118,110,.14); border-radius: 999px;
            padding: 8px 13px; background: white; color: #14756d; font-size: .62rem;
            font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
            box-shadow: 0 12px 28px rgba(12,82,83,.06);
        }
        .landing-hero h1 {
            margin: 1.7rem 0 .8rem; color: #112b30; font-family: 'DM Serif Display', serif;
            font-size: clamp(3.8rem, 9vw, 7.5rem); font-weight: 500; line-height: .79; letter-spacing: -.07em;
        }
        .landing-hero h1 em { color: #0d9488; font-style: normal; }
        .landing-hero p { max-width: 500px; margin: 1.5rem auto 1.8rem; color: #60777a; font-size: 1rem; line-height: 1.65; }
        .landing-flow {
            display: grid; grid-template-columns: 1.35fr .65fr; gap: 14px; margin-top: 4.5rem;
            padding: 14px; border: 1px solid rgba(15,118,110,.11); border-radius: 26px;
            background: rgba(255,255,255,.88); box-shadow: 0 28px 70px rgba(12,82,83,.13); text-align: left;
        }
        .landing-steps { padding: 18px; border-radius: 18px; background: #f4fbf8; }
        .landing-steps > span, .landing-review > span { color: #14756d; font-size: .6rem; font-weight: 700; letter-spacing: .12em; }
        .step-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 9px; margin-top: 14px; }
        .step-card { min-height: 122px; border: 1px solid; border-radius: 13px; padding: 13px; }
        .step-card b, .step-card strong, .step-card small { display: block; }.step-card b { font-size: .58rem; opacity: .7; }.step-card strong { margin-top: 21px; font-size: .96rem; }.step-card small { margin-top: 4px; font-size: .64rem; opacity: .72; }
        .step-source { border-color: #f0dfbd; background: #fff9ed; color: #a26918; }.step-review { border-color: #cce9e3; background: #ecfaf6; color: #14756d; }.step-export { border-color: #123f46; background: #06343d; color: #effaf8; }
        .landing-review { border-radius: 18px; padding: 23px 20px; background: #06343d; color: white; }.landing-review h2 { margin: 12px 0 21px; font-family: 'DM Serif Display', serif; font-size: 1.7rem; line-height: .98; letter-spacing: -.045em; }.review-point { margin-top: 8px; border: 1px solid rgba(255,255,255,.1); border-radius: 9px; padding: 8px; background: rgba(255,255,255,.06); color: #e7f7f4; font-size: .68rem; font-weight: 600; }
        @media(max-width: 640px) { .landing-nav { margin-bottom: 3.5rem; }.landing-nav span { display: none; }.landing-flow { grid-template-columns: 1fr; }.landing-hero h1 { font-size: 4.3rem; }.step-card { min-height: 105px; padding: 10px; }.step-card strong { margin-top: 17px; font-size: .82rem; } }
    </style>
    <div class="landing-nav">
        <div class="landing-brand"><div class="landing-mark"></div><div><strong>DETECTFRAME</strong><small>VISION REVIEW</small></div></div>
        <span>Human-guided computer vision</span>
    </div>
    <div class="landing-hero">
        <div class="landing-kicker">Evidence-led object detection</div>
        <h1>Images,<br><em>made legible.</em></h1>
        <p>From raw frames to reviewed evidence. Keep every model signal visible, understandable, and under your control.</p>
    </div>
    """, unsafe_allow_html=True)

    _, enter_column, _ = st.columns([1.1, 1, 1.1])
    with enter_column:
        if st.button("Enter review workspace  →", key="enter_workspace", use_container_width=True):
            st.session_state["show_workspace"] = True
            st.rerun()

    st.markdown("""
    <div class="landing-flow">
        <div class="landing-steps"><span>EVIDENCE FLOW</span><div class="step-grid">
            <div class="step-card step-source"><b>01</b><strong>Frame</strong><small>Temporary source</small></div>
            <div class="step-card step-review"><b>02</b><strong>Review</strong><small>Human in the loop</small></div>
            <div class="step-card step-export"><b>03</b><strong>Evidence</strong><small>Confirmed output</small></div>
        </div></div>
        <div class="landing-review"><span>REVIEW STATUS</span><h2>Nothing leaves the frame without you.</h2>
            <div class="review-point">Class and confidence remain visible</div>
            <div class="review-point">Uncertain signals stay inspectable</div>
            <div class="review-point">Export follows deliberate review</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

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
if st.sidebar.button("← Landing page", use_container_width=True):
    st.session_state["show_workspace"] = False
    st.rerun()

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

# Brand Header
st.markdown("""
<div class='brand-header'>
    <div class='brand-logo'>+</div>
    <div class='leading-none'>
        <span class='brand-title'>YOLO-Detect</span>
        <div class='brand-subtitle'>Object Intelligence</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Title Header (ClinicOCR layout style)
st.markdown("<div class='hero-heading'>Object detection,<br><span class='hero-heading-teal'>made clear.</span></div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>A real-time deep learning computer vision dashboard with Pandas-driven logs and interactive analytics.</div>", unsafe_allow_html=True)

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
            st.markdown(f"""
            <div class='evidence-step'>
                <span class='evidence-label label-cyan'>Detections</span>
                <h3 style='color:#0f766e; font-family: "DM Serif Display", serif; font-size: 2.2rem; margin: 8px 0 0 0;'>{len(df_dets)}</h3>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class='evidence-step'>
                <span class='evidence-label label-amber'>Latency</span>
                <h3 style='color:#b45309; font-family: "DM Serif Display", serif; font-size: 2.2rem; margin: 8px 0 0 0;'>{latency:.1f} ms</h3>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            avg_conf = df_dets["confidence"].mean() if not df_dets.empty else 0.0
            st.markdown(f"""
            <div class='evidence-step'>
                <span class='evidence-label label-slate'>Avg Confidence</span>
                <h3 style='color:#475569; font-family: "DM Serif Display", serif; font-size: 2.2rem; margin: 8px 0 0 0;'>{avg_conf:.1%}</h3>
            </div>
            """, unsafe_allow_html=True)
            
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
            <div class='evidence-step'>
                <span class='evidence-label label-cyan'>Total Logs</span>
                <p style='margin-top: 10px; font-size: 0.85rem; color: #64748b;'>Total Detections Logged</p>
                <h2 style='color:#0f766e; font-family: "DM Serif Display", serif; font-size: 2.5rem; margin: 5px 0;'>{total_records}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_met2:
            st.markdown(f"""
            <div class='evidence-step'>
                <span class='evidence-label label-amber'>Categories</span>
                <p style='margin-top: 10px; font-size: 0.85rem; color: #64748b;'>Unique Class Categories</p>
                <h2 style='color:#b45309; font-family: "DM Serif Display", serif; font-size: 2.5rem; margin: 5px 0;'>{unique_classes}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_met3:
            st.markdown(f"""
            <div class='evidence-step'>
                <span class='evidence-label label-slate'>Mean Score</span>
                <p style='margin-top: 10px; font-size: 0.85rem; color: #64748b;'>Average Confidence</p>
                <h2 style='color:#475569; font-family: "DM Serif Display", serif; font-size: 2.5rem; margin: 5px 0;'>{avg_confidence:.1%}</h2>
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
