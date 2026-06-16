# Skill: Image Preprocessing & Masking (Phase 2)

This document covers U²-Net segmentation, captioning, and image resizing.

## 1. Clothing Segmentation (U²-Net)
- **Why U²-Net**: It is a lightweight ($\sim 44$ MB or smaller) network ideal for local CPUs, avoiding the high VRAM usage of SAM.
- **CPU Execution**: Load and run the U²-Net model exclusively on the CPU.
- **Output Mask**: Convert the U²-Net output into a binary mask (0 for background, 255 for target clothing area) saved as PNG in `data/processed/masks/`.

## 2. Caption Generation (BLIP)
- Use `Salesforce/blip-image-captioning-base` to generate description captions.
- Run the BLIP pipeline on **CPU** or **GPU** (GPU only if Stable Diffusion is not loaded).
- Generate a text file for each processed image, matching the base filename (e.g., `image_001.png` and `image_001.txt`).

## 3. Resizing & Padding (512x512)
Stable Diffusion 1.5 expects 512x512 inputs. Preserve aspect ratio to avoid distortion:
- Resize the longer edge of the image to 512 pixels.
- Pad the shorter edge equally on both sides (letterboxing) with a neutral color (e.g., black or white) to reach exactly 512x512 pixels.
- Apply the identical transformation (resize + pad) to the corresponding mask image.
