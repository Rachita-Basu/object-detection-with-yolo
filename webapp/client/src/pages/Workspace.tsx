/**
 * Original-workspace restoration: this page reinterprets the selected repository's Streamlit
 * object-detection dashboard as a responsive React interface while preserving its original controls and task flow.
 */
import "./workspace.css";
import {
  BarChart3,
  Camera,
  Check,
  ChevronDown,
  CircleHelp,
  FileImage,
  Gauge,
  Image as ImageIcon,
  Play,
  RotateCcw,
  Trash2,
  Upload,
  Video,
  Webcam,
} from "lucide-react";
import { type ChangeEvent, useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import { useLocation } from "wouter";

type Tab = "image" | "video" | "webcam" | "analytics";

const sampleImage = "/manus-storage/detectframe-street_74d395bb.jpg";
const detectionRows = [
  ["person", "0.967", "(142, 118)", "(299, 551)"],
  ["bicycle", "0.914", "(371, 223)", "(658, 603)"],
  ["car", "0.896", "(694, 186)", "(1056, 531)"],
  ["traffic light", "0.742", "(1052, 48)", "(1094, 161)"],
];

export default function Workspace() {
  const [, setLocation] = useLocation();
  const [activeTab, setActiveTab] = useState<Tab>("image");
  const [modelSize, setModelSize] = useState("Nano (Fastest, ~12MB)");
  const [confidence, setConfidence] = useState(0.25);
  const [iou, setIou] = useState(0.45);
  const [selectAll, setSelectAll] = useState(true);
  const [imageMode, setImageMode] = useState<"sample" | "upload">("sample");
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [videoMode, setVideoMode] = useState<"sample" | "upload">("sample");
  const [videoName, setVideoName] = useState<string | null>(null);
  const [webcamActive, setWebcamActive] = useState(false);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const imageInput = useRef<HTMLInputElement>(null);
  const videoInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (videoRef.current && stream) videoRef.current.srcObject = stream;
    return () => stream?.getTracks().forEach((track) => track.stop());
  }, [stream]);

  const onImageUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const image = event.target.files?.[0];
    if (!image) return;
    setUploadedImage(URL.createObjectURL(image));
    setImageMode("upload");
    toast("Custom image loaded", { description: "The visual detection preview now uses your selected file." });
  };

  const onVideoUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const video = event.target.files?.[0];
    if (!video) return;
    setVideoName(video.name);
    setVideoMode("upload");
    toast("Video ready", { description: "Run processing to start the demonstration video workflow." });
  };

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      setStream(mediaStream);
      setWebcamActive(true);
      toast("Camera preview enabled", { description: "Your local browser stream is now visible in the workspace." });
    } catch {
      setWebcamActive(false);
      toast("Camera unavailable", { description: "Grant browser camera access or check that a camera is connected." });
    }
  };

  const stopCamera = () => {
    stream?.getTracks().forEach((track) => track.stop());
    setStream(null);
    setWebcamActive(false);
  };

  const resetLogs = () => toast("Session analytics cleared", { description: "No persistent data was removed." });
  const currentImage = imageMode === "upload" && uploadedImage ? uploadedImage : sampleImage;

  return (
    <main className="yolo-workspace">
      <aside className="yolo-sidebar">
        <button className="yolo-brand" onClick={() => setLocation("/")} type="button" aria-label="Return to landing page">
          <span>+</span><div><strong>YOLO-Detect</strong><small>Object intelligence</small></div>
        </button>
        <div className="sidebar-rule" />
        <h2><Gauge size={17} /> Control panel</h2>

        <section className="sidebar-section">
          <label htmlFor="model-size">Choose YOLO Model Size</label>
          <div className="select-wrap"><select id="model-size" onChange={(event) => setModelSize(event.target.value)} value={modelSize}><option>Nano (Fastest, ~12MB)</option><option>Small (Balanced, ~22MB)</option><option>Medium (Accurate, ~50MB)</option></select><ChevronDown size={14} /></div>
          <div className="model-status"><span className="status-pulse" /><div><strong>Model loaded successfully</strong><small>{modelSize.split(" ")[0].toLowerCase()} weights ready</small></div></div>
        </section>

        <section className="sidebar-section range-section">
          <h3>Threshold parameters</h3>
          <label htmlFor="confidence">Confidence threshold <b>{confidence.toFixed(2)}</b></label>
          <input id="confidence" max="1" min="0" onChange={(event) => setConfidence(Number(event.target.value))} step="0.05" type="range" value={confidence} />
          <label htmlFor="iou">IoU threshold <b>{iou.toFixed(2)}</b></label>
          <input id="iou" max="1" min="0" onChange={(event) => setIou(Number(event.target.value))} step="0.05" type="range" value={iou} />
        </section>

        <section className="sidebar-section class-section">
          <h3>Class filtering</h3>
          <label className="checkbox-row"><input checked={selectAll} onChange={(event) => setSelectAll(event.target.checked)} type="checkbox" /><span>Select all classes</span></label>
          <div className="class-chips">{["person", "car", "bicycle", "dog", "cat"].map((item) => <span className={selectAll ? "chip-active" : ""} key={item}>{item}</span>)}</div>
        </section>

        <button className="clear-logs" onClick={resetLogs} type="button"><Trash2 size={15} /> Clear analytics logs</button>
        <section className="project-note"><h3>About project</h3><p><strong>Object Detection using YOLO</strong> is a real-time 2D object-detection, classification, and visual-analytics project.</p><span><CircleHelp size={13} /> Browser demo interface</span></section>
      </aside>

      <div className="yolo-main">
        <header className="yolo-header"><button onClick={() => setLocation("/")} type="button">← Back to DetectFrame</button><span>Object detection workspace</span></header>
        <section className="yolo-intro">
          <div className="yolo-wordmark"><span>+</span><div><strong>YOLO-Detect</strong><small>Object intelligence</small></div></div>
          <h1>Object detection,<br /><em>made clear.</em></h1>
          <p>A real-time deep learning computer-vision dashboard with session logs and interactive analytics.</p>
        </section>

        <nav className="yolo-tabs" aria-label="Detection modes">
          {[
            ["image", ImageIcon, "Image detection"],
            ["video", Video, "Video processing"],
            ["webcam", Webcam, "Live webcam"],
            ["analytics", BarChart3, "Analytics dashboard"],
          ].map(([id, Icon, label]) => <button className={activeTab === id ? "tab-active" : ""} key={id as string} onClick={() => setActiveTab(id as Tab)} type="button"><Icon size={16} /> {label as string}</button>)}
        </nav>

        {activeTab === "image" && <section className="tab-page image-tab">
          <div className="tab-heading"><div><span>Image detection</span><h2>Static image detection</h2><p>Upload an image file or run the detector on the supplied sample image.</p></div><div className="tip-card"><CircleHelp size={16} /> Adjust thresholds and target classes in the control panel to filter results.</div></div>
          <div className="source-card"><div><p>Choose image input source</p><div className="segmented"><button className={imageMode === "sample" ? "segment-active" : ""} onClick={() => setImageMode("sample")} type="button">Use sample image</button><button className={imageMode === "upload" ? "segment-active" : ""} onClick={() => imageInput.current?.click()} type="button">Upload custom image</button></div></div><button className="upload-outline" onClick={() => imageInput.current?.click()} type="button"><Upload size={16} /> Add image</button><input accept="image/*" className="visually-hidden" onChange={onImageUpload} ref={imageInput} type="file" /></div>
          <h3 className="section-title">Inference &amp; visualizations</h3>
          <div className="image-comparison"><article><h3>Original image</h3><img src={currentImage} alt="Selected object-detection source" /></article><article className="annotated-image"><h3>Annotated result <span>YOLOv8</span></h3><img src={currentImage} alt="Annotated object detection result" /><span className="object-box object-box-one">person <b>0.97</b></span><span className="object-box object-box-two">bicycle <b>0.91</b></span><span className="object-box object-box-three">car <b>0.89</b></span></article></div>
          <div className="metric-row"><Metric label="Detections" value="4" tone="teal" /><Metric label="Latency" value="28.4 ms" tone="amber" /><Metric label="Avg confidence" value="91.4%" tone="slate" /></div>
          <article className="logs-card"><div className="logs-heading"><div><span>Session log</span><h3>Detected objects</h3></div><button onClick={() => toast("CSV download is ready when connected to the inference service.")} type="button">Download detection CSV</button></div><div className="table-wrap"><table><thead><tr><th>Class</th><th>Confidence</th><th>Top-left</th><th>Bottom-right</th></tr></thead><tbody>{detectionRows.map((row) => <tr key={row[0]}>{row.map((cell) => <td key={cell}>{cell}</td>)}</tr>)}</tbody></table></div></article>
        </section>}

        {activeTab === "video" && <section className="tab-page"><div className="tab-heading"><div><span>Video processing</span><h2>Real-time video detection</h2><p>Upload a video to analyze it frame-by-frame and visualise dynamic detection trends.</p></div></div><div className="video-layout"><article className="video-source-panel"><p>Choose video input source</p><div className="segmented"><button className={videoMode === "sample" ? "segment-active" : ""} onClick={() => setVideoMode("sample")} type="button">Use sample video</button><button className={videoMode === "upload" ? "segment-active" : ""} onClick={() => videoInput.current?.click()} type="button">Upload custom video</button></div><input accept="video/*" className="visually-hidden" onChange={onVideoUpload} ref={videoInput} type="file" /><div className="video-file-name">{videoMode === "upload" && videoName ? videoName : "shuttle.mp4 · supplied sample"}</div><button className="run-inference" onClick={() => toast("Video processing simulation started", { description: "Connect the Python YOLO service to process every frame." })} type="button"><Play size={16} /> Process video &amp; run inference</button></article><article className="chart-placeholder"><div><BarChart3 size={24} /><h3>Detection count over time</h3><p>Frame-level activity will appear here after processing.</p></div><span className="chart-line" /></article></div></section>}

        {activeTab === "webcam" && <section className="tab-page"><div className="tab-heading"><div><span>Live webcam</span><h2>Live webcam stream detection</h2><p>Run real-time detection using a local browser camera feed.</p></div></div><div className="webcam-layout"><article className="camera-controls"><div className="camera-control-head"><Camera size={19} /><div><h3>Camera device</h3><p>Grant browser access when you activate the feed.</p></div></div><label htmlFor="camera-index">Camera device index</label><div className="camera-index"><input defaultValue="0" id="camera-index" max="10" min="0" type="number" /><span>Primary device</span></div><button className={webcamActive ? "webcam-toggle webcam-toggle-on" : "webcam-toggle"} onClick={webcamActive ? stopCamera : startCamera} type="button"><span /> {webcamActive ? "Deactivate live webcam feed" : "Activate live webcam feed"}</button><div className="camera-help"><CircleHelp size={15} /> Browser camera access is required for the live preview.</div></article><article className="camera-preview">{webcamActive ? <video autoPlay muted playsInline ref={videoRef} /> : <div className="camera-empty"><Webcam size={34} /><h3>Camera preview idle</h3><p>Activate the live webcam feed to begin a local preview.</p></div>} {webcamActive && <div className="camera-live"><span /> LIVE · local browser stream</div>}</article></div></section>}

        {activeTab === "analytics" && <section className="tab-page"><div className="tab-heading"><div><span>Analytics dashboard</span><h2>Session analytics dashboard</h2><p>Examine aggregated statistics and insight from detections captured in this session.</p></div></div><div className="metric-row analytics-metrics"><Metric label="Total logs" value="42" tone="teal" /><Metric label="Categories" value="4" tone="amber" /><Metric label="Mean score" value="91.4%" tone="slate" /></div><div className="analytics-grid"><article className="bar-chart-card"><h3>Object counts by class</h3>{[["person", 86], ["bicycle", 56], ["car", 71], ["traffic light", 32]].map(([label, value]) => <div className="bar-entry" key={label as string}><span>{label as string}</span><i><b style={{ width: `${value}%` }} /></i><strong>{value as number}</strong></div>)}</article><article className="distribution-card"><h3>Confidence distribution</h3><div className="distribution-plot"><span className="plot-axis plot-y" /><span className="plot-axis plot-x" /><i className="plot-range plot-range-one" /><i className="plot-range plot-range-two" /><i className="plot-range plot-range-three" /><i className="plot-range plot-range-four" /></div><p>Confidence levels remain grouped by class for the active session.</p></article></div></section>}
      </div>
    </main>
  );
}

function Metric({ label, value, tone }: { label: string; value: string; tone: "teal" | "amber" | "slate" }) {
  return <article className={`yolo-metric metric-${tone}`}><span>{label}</span><strong>{value}</strong></article>;
}
