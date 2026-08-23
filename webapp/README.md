# DetectFrame Web UI

This directory contains the completed React/Vite frontend delivered alongside the original Streamlit YOLO application, which remains unchanged in the repository root.

The web UI provides a ClinicOCR-inspired landing page at `/` and the restored original-style object-detection workspace at `/workspace`. The workspace includes the repository’s original model-selection, threshold, class-filter, image, video, webcam, and analytics flows as an interactive frontend. Browser camera preview is available when the user grants permission; server-side YOLO inference remains available through the original Python application and can be connected as a backend integration.

## Run locally

```bash
cd webapp
pnpm install
pnpm dev
```

Use `pnpm check` for type checking and `pnpm build` for a production build.
