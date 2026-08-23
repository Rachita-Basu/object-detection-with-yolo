# Reference Design Direction

## Ground-Truth Reference

The interface should adapt the visual language of [ClinicOCR](https://clinic-ocr-app.vercel.app/) rather than reproduce its clinical workflow. The accessible reference establishes a full-viewport, low-key secure-session state in a deep blue-green field with restrained, pale text. Its public project description positions the product as a review-first workspace: an image is processed, an editable result is reviewed, and only then is it saved. The YOLO interface will preserve that calm, trustworthy, operational feeling while changing the domain from prescriptions to image-based object detection.

> **Reference principles:** understated clinical-grade dark surface, clear task hierarchy, review before commitment, concise status language, and composed rather than decorative motion.

## Selected Approach: Field Console

### Design Movement

Field Console is informed by high-reliability clinical workstations and contemporary scientific-instrument interfaces. It uses a dark, spectral background and precise information architecture to make the detection result feel inspectable rather than theatrical.

### Core Principles

The UI will make the image the main artifact, use a persistent navigation rail for orientation, distinguish detection confidence without visual noise, and keep every irreversible-looking action explicit. Surfaces will be quietly layered through tonal shifts instead of heavy borders or floating-card overload.

### Color Philosophy

Near-black **deep teal** establishes the secure, focused reference mood. Desaturated blue-green surfaces create visual depth, while an unmistakable **signal coral** accent marks active controls, detected regions, and review attention. Soft cloud text supports sustained reading without the glare of pure white.

### Layout Paradigm

The desktop workspace is an asymmetric split console. A narrow left rail provides task context; the center holds the image and detection canvas; a deliberately slimmer right-side inspector organizes labels, confidence, and output actions. On small screens, the panels resolve into a vertical review flow without losing hierarchy.

### Signature Elements

The design repeats three motifs: crosshair-like detection brackets, fine coordinate-grid traces within media panels, and small status lozenges that read like instrument telemetry. The brand symbol will be a modular aperture-and-box mark rather than typography.

### Interaction Philosophy

Interactions should feel careful and physical. Uploading changes the workspace state, selecting a detection brings its matching confidence record forward, and toggling overlays directly changes what the user can inspect. Placeholder actions provide candid feedback rather than pretending to complete an unavailable model task.

### Animation

Transitions are brief and explanatory: panels fade and lift over 180–240ms, results stagger in at 40ms intervals, and selected detections receive a restrained outline pulse. Motion uses transform and opacity only, obeys reduced-motion preferences, and never delays keyboard-first operation.

### Typography System

**DM Sans** provides the utilitarian body and UI voice, while **Sora** supplies compact, geometric display hierarchy. Headlines are tightly tracked and calm; metadata is smaller, tabular where useful, and more muted than the primary task content.

### Brand Essence

**DetectFrame is a deliberate review workspace for teams turning raw imagery into explainable YOLO detections.** Its personality is exacting, calm, and observant.

### Brand Voice

Headlines are direct and evidence-led, CTAs are short verbs, and microcopy treats the user as a capable operator. The voice avoids generic onboarding language. Example lines: “Frame the evidence.” and “Review every signal before export.”

### Wordmark & Logo

The logo is a bold aperture assembled from four cropped detection-corner brackets with a coral target dot at its center. The wordmark pairs this mark with a custom-spaced Sora label, never a default text treatment.

### Signature Brand Color

**Signal Coral — `#F4755C`** is the ownable brand color used only for primary intent, selected detections, and attention-critical states.

## Style Decisions

The primary identity always includes the modular aperture-and-box mark with its coral target dot; the name alone is never the only brand identifier. Signal Coral remains exclusive to primary intent, selected evidence, and review-critical attention, while other classification colors stay muted and spectral. Every major surface carries at least one Field Console motif—detection brackets, coordinate-grid traces, telemetry lozenges, or aperture geometry—so the workspace reads as a unified scientific instrument.

## Revised Two-Page Architecture

The home route becomes a bright, editorial landing page inspired by ClinicOCR’s public-facing sequence: a spacious light-teal hero, a fixed but compacting navigation bar, a large staged headline, a visual evidence-flow panel, and a dark secure-workspace invitation. The language changes from prescription review to image intelligence while keeping ClinicOCR’s calm, credible, human-controlled feeling.

The existing deep-teal Field Console remains intact as the `/workspace` route. This creates a purposeful transition: **the landing page explains why evidence should be reviewed, while the workspace lets the operator inspect it.** Both pages share the DetectFrame aperture mark, Signal Coral moments of primary intent, and concise, evidence-led copy.
