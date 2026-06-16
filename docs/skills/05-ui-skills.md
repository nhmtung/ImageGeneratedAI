# Skill: Gradio UI Development (Phase 5)

This document covers local web interface construction using Gradio.

## 1. Component Interface Layout
- **Image Input**: Use `gr.Image(tool="editor", type="numpy")` to support image uploads and manual mask brushing directly in the UI.
- **Config Sliders**: Provide `gr.Slider` for:
  - Inference steps (range: 15-30, default: 20 to control latency).
  - Guidance scale / CFG (range: 5.0-12.0, default: 7.5).
  - Strength (inpainting overlap, range: 0.0-1.0, default: 0.8).
- **Control Buttons**: Include clear buttons for "Generate", "Clear", and toggles like "NSFW Mode" (visible only if `ENABLE_NSFW=true` in `.env`).

## 2. Asynchronous Execution
- Prevent freezing the web UI during generation.
- Design execution handlers to run in a separate thread or use Gradio's built-in queue system:
  ```python
  import gradio as gr
  demo = gr.Interface(...)
  demo.queue()  # Enables concurrency and displays progress bar
  demo.launch()
  ```

## 3. UI responsiveness
- Limit the preview image sizes to prevent long browser transfers.
- Display a progress indicator or step-by-step logs directly in a `gr.Textbox` to show status (e.g., "Step 1/3: Segmenting clothing on CPU...").
