# Skill: Data Crawling (Phase 1)

This document provides step-by-step guidance and best practices for implementing the data crawling phase.

## 1. API Rate Limits & Mitigation
When Crawling from Unsplash and Pexels APIs:
- **Exponential Backoff**: Implement retry logic with exponential backoff for HTTP requests.
- **Random Delays**: Introduce random sleep intervals between requests (`time.sleep(random.uniform(1.0, 3.0))`) to mimic human behavior and avoid trigger blocks.
- **API Keys**: Read API keys dynamically from environment variables (`UNSPLASH_KEY`, `PEXELS_KEY`).

## 2. Person Filtering (YOLOv8n)
To ensure crawled dataset quality:
- Run YOLOv8n **strictly on the CPU** to save GPU memory.
- Load the model:
  ```python
  from ultralytics import YOLO
  model = YOLO("yolov8n.pt")  # Auto-downloads lightweight model
  ```
- Predict with confidence threshold $\ge 0.7$ and verify if class `0` (person) is detected in the image boundaries.

## 3. Metadata Saving
Save metadata in a structured JSON file at `data/raw/metadata.json`.
Format:
```json
{
  "images": [
    {
      "filename": "unsplash_001.jpg",
      "source": "Unsplash",
      "url": "https://...",
      "resolution": [1920, 1080],
      "has_person": true,
      "crawled_at": "2026-06-16T22:36:00Z"
    }
  ]
}
```
