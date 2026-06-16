# Skill: LoRA Fine-Tuning (Phase 3)

This document outlines the training configurations and environments for Stable Diffusion 1.5 LoRA.

## 1. LoRA Configuration
- **Base Model**: `runwayml/stable-diffusion-v1-5` (fp16)
- **Rank / Alpha**: `rank=32` / `alpha=32` (Higher ranks exceed memory limits; lower ranks lack capability).
- **Optimizer & Learning Rate**: AdamW with `lr=1e-4`.
- **Batch Size**: Hard limit `batch_size=1`.
- **Gradient Accumulation**: Set to 4 steps if higher effective batch size is needed.

## 2. Training Pipelines
- Leverage HuggingFace `diffusers` + `peft` libraries to inject LoRA layers into the UNet attention blocks.
- Train the Text Encoder only if dataset contains highly specific new tokens. Otherwise, freeze it to save memory.

## 3. Training Execution (Colab/RunPod Fallback)
- **Local Limit**: Training on a 2 GB GPU will trigger CUDA Out-Of-Memory (OOM) errors.
- **Remote Training**:
  - Run the `scripts/train_lora.py` script on a free Google Colab (T4 GPU, 16 GB VRAM) or cheap RunPod instance.
  - Export checkpoints as `.safetensors`.
  - Download the final adapter (e.g., `lora_fashion.safetensors` or `lora_nsfw.safetensors`) to the local `models/` directory for inference.
