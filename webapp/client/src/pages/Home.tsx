/**
 * Landing design: ClinicOCR-inspired editorial introduction with a bright evidence-flow hero;
 * it intentionally hands off to the deep-teal Field Console workspace at /workspace.
 */
import "./landing.css";
import { Button } from "@/components/ui/button";
import {
  ArrowRight,
  Check,
  ChevronDown,
  FileImage,
  ScanLine,
  ShieldCheck,
  Sparkles,
  Target,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useLocation } from "wouter";

function ApertureBrand() {
  return (
    <span className="landing-aperture" aria-hidden="true">
      <i className="landing-corner landing-corner-tl" />
      <i className="landing-corner landing-corner-tr" />
      <i className="landing-corner landing-corner-bl" />
      <i className="landing-corner landing-corner-br" />
      <b />
    </span>
  );
}

const workflowSteps = [
  {
    number: "01",
    title: "Bring the frame",
    description: "Add an image from the field, the lab, or the archive. The original remains the visual evidence.",
    icon: FileImage,
    note: "Source image",
  },
  {
    number: "02",
    title: "Review each signal",
    description: "Inspect the model output in context. Confidence, class, and location stay visible to the operator.",
    icon: ScanLine,
    note: "Operator-guided",
  },
  {
    number: "03",
    title: "Export with intent",
    description: "Confirm meaningful detections before they become shareable evidence or structured output.",
    icon: ShieldCheck,
    note: "Evidence-led",
  },
];

export default function Home() {
  const [, setLocation] = useLocation();
  const [compactNav, setCompactNav] = useState(false);

  useEffect(() => {
    const updateNavigation = () => setCompactNav(window.scrollY > 24);
    updateNavigation();
    window.addEventListener("scroll", updateNavigation, { passive: true });
    return () => window.removeEventListener("scroll", updateNavigation);
  }, []);

  const openWorkspace = () => setLocation("/workspace");
  const scrollTo = (id: string) => document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });

  return (
    <main className="landing-page">
      <section className="landing-hero" id="top">
        <div className="hero-halo hero-halo-left" aria-hidden="true" />
        <div className="hero-halo hero-halo-right" aria-hidden="true" />

        <nav className={`landing-nav ${compactNav ? "landing-nav-compact" : ""}`} aria-label="Landing navigation">
          <button className="landing-brand" onClick={() => scrollTo("top")} type="button">
            <ApertureBrand />
            <span><strong>DETECTFRAME</strong><small>VISION REVIEW</small></span>
          </button>
          <div className="landing-nav-links">
            <button onClick={() => scrollTo("top")} type="button">Home</button>
            <button onClick={() => scrollTo("workflow")} type="button">Workflow</button>
            <button onClick={() => scrollTo("secure-entry")} type="button">Approach</button>
          </div>
          <Button className="landing-nav-cta" onClick={openWorkspace} variant="outline">
            Open workspace <ArrowRight size={15} />
          </Button>
        </nav>

        <div className="landing-hero-copy">
          <div className="landing-kicker"><span><Target size={12} /></span> Human-guided computer vision</div>
          <h1>Images,<br /><em>made legible.</em></h1>
          <p>From raw frames to reviewed evidence. DetectFrame gives every model signal a clear place to be seen, understood, and confirmed.</p>
          <Button className="landing-primary-cta" onClick={openWorkspace}>
            Enter review workspace <ArrowRight size={17} />
          </Button>
        </div>

        <article className="landing-evidence-card" aria-label="Evidence flow overview">
          <div className="evidence-main">
            <div className="evidence-card-heading">
              <div><span className="live-dot" /> EVIDENCE FLOW</div>
              <span>Operator controlled</span>
            </div>
            <div className="evidence-stage">
              <div className="evidence-signal-line" aria-hidden="true"><i /></div>
              <div className="evidence-step evidence-step-source">
                <span>01</span><strong>Frame</strong><small>Temporary source</small><FileImage size={20} />
              </div>
              <div className="evidence-step evidence-step-review">
                <span>02</span><strong>Review</strong><small>Human in the loop</small><ScanLine size={20} />
              </div>
              <div className="evidence-step evidence-step-export">
                <span>03</span><strong>Evidence</strong><small>Confirmed output</small><Check size={20} />
              </div>
            </div>
          </div>
          <div className="evidence-assurance">
            <div className="assurance-rings" aria-hidden="true" />
            <p className="assurance-label">Review status</p>
            <h2>Nothing leaves the frame without you.</h2>
            {[
              "Class and confidence remain visible",
              "Uncertain signals stay inspectable",
              "Export follows deliberate review",
            ].map((item, index) => <div className="assurance-item" key={item}><span>{index + 1}</span>{item}</div>)}
          </div>
        </article>
      </section>

      <section className="landing-workflow" id="workflow">
        <div className="workflow-heading">
          <div className="workflow-heading-icon"><Sparkles size={17} /></div>
          <div><span>THE REVIEW PATH</span><h2>Clear evidence, at every step.</h2></div>
        </div>
        <div className="workflow-layout">
          <div className="workflow-visual">
            <div className="workflow-visual-glow" />
            <img src="/manus-storage/detectframe-desk_b0539586.jpg" alt="A workbench analysis frame" />
            <div className="visual-topline"><ApertureBrand /><span>ANALYSIS FRAME · 0038</span></div>
            <div className="visual-detection visual-detection-one"><b>Object</b><span>96.8%</span></div>
            <div className="visual-detection visual-detection-two"><b>Tool</b><span>94.2%</span></div>
          </div>
          <div className="workflow-steps">
            {workflowSteps.map((step) => {
              const Icon = step.icon;
              return (
                <article className="workflow-step" key={step.number}>
                  <div className="workflow-number">{step.number}</div>
                  <div><div className="workflow-step-title"><Icon size={16} /><h3>{step.title}</h3></div><p>{step.description}</p><span>{step.note}</span></div>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="landing-secure-entry" id="secure-entry">
        <div className="secure-copy">
          <span className="secure-label">A considered workspace</span>
          <h2>Your evidence workspace is ready when you are.</h2>
          <p>Open a calm, precise console built for reviewing what the model found—not just what it predicted.</p>
          <Button className="secure-entry-cta" onClick={openWorkspace}>
            Open DetectFrame <ArrowRight size={17} />
          </Button>
        </div>
        <div className="secure-illustration" aria-hidden="true">
          <div className="secure-ring secure-ring-one" />
          <div className="secure-ring secure-ring-two" />
          <div className="secure-workspace-card"><ApertureBrand /><div><strong>Protected review</strong><span>Workspace access ready</span></div><ShieldCheck size={18} /></div>
          <div className="secure-checklist">{["Evidence context retained", "Operator review required", "Export state confirmed"].map((item, index) => <span key={item}><b>{index + 1}</b>{item}</span>)}</div>
        </div>
      </section>

      <footer className="landing-footer"><div className="landing-brand"><ApertureBrand /><span><strong>DETECTFRAME</strong><small>VISION REVIEW</small></span></div><span>Evidence-led computer vision.</span><button onClick={openWorkspace} type="button">Workspace <ChevronDown size={14} /></button></footer>
    </main>
  );
}
