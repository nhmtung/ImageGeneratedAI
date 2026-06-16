# AGENTS.md — Project Constitution

> The definitive ruleset for any AI Agent operating on this repository.
> Every directive in this document is **non-negotiable** unless the Developer explicitly overrides it.

---

## 1. Project Identity & Context

| Field | Value |
|---|---|
| **Project Name** | AI Fashion Editor (Local) |
| **Core Mission** | Offline image editing — Virtual Try-On (Inpainting) and clothing removal (NSFW) — optimized for Vietnamese and East Asian women. |
| **Target Users** | Single developer/researcher on a local machine. Not a public service. |
| **Development Method** | Vibe Code — rapid AI-assisted development with Cursor / Claude / Gemini agents. |
| **NSFW Support** | Yes. Private, local research and personal use only. Never shared or published. |

### Critical Hardware Constraint

| Component | Specification |
|---|---|
| **Machine** | Acer Aspire 3 |
| **CPU** | Intel Core i5-1035G1 @ 1.00GHz (4C/8T) |
| **RAM** | 7.8 GB DDR4 |
| **GPU** | NVIDIA GeForce MX330 — **2 GB VRAM** (CUDA Compute 6.1) |
| **OS** | Windows 11 Home |

**Strategy**: LoRA (rank ≤ 32) on **Stable Diffusion 1.5 only**. Full fine-tuning, SDXL, SD3, and Flux are physically impossible on this hardware.

---

## 2. Core Principles (The Ten Commandments)

Every AI Agent working on this project **must** obey the following rules without exception:

1. **Memory-First.** Peak VRAM usage must **never** exceed **1.8 GB**. Always use `torch.float16`, enable `attention_slicing`, enable `sequential_cpu_offload`, and call `torch.cuda.empty_cache()` after every pipeline run. No exceptions.

2. **One Model at a Time.** You must **never** load two models on the GPU simultaneously. Unload model A (`del model` + `torch.cuda.empty_cache()`) before loading model B. Segmentation runs on **CPU**. Stable Diffusion runs on **GPU**.

3. **NEVER Suggest SDXL.** Do not suggest, recommend, or import SDXL, SD 2.x, SD 3.x, Flux, DALL-E, or any model requiring > 2 GB VRAM. This hardware cannot run them. Period.

4. **NEVER Suggest Cloud-Based Inference.** All inference must run 100% offline on the local machine. No API calls to Replicate, RunPod, HuggingFace Inference, or any remote endpoint. The only exception is the initial data crawling phase (Phase 1).

5. **Offline-Only.** Zero data leaves the local machine during inference. No telemetry, no analytics, no tracking. Disable all third-party data collection features.

6. **Privacy & NSFW.** NSFW features are permitted strictly for local, private research and personal use. **NEVER** push NSFW data, NSFW model weights, or NSFW outputs to any public repository, cloud storage, or shared drive.

7. **Phase Discipline.** Always follow the Phase Loop (Section 3). Never skip phases. Never start Phase N+1 before Phase N is marked `Completed` in the master plan.

8. **Test Before Commit.** Every code change must be tested (at minimum: a manual smoke test on one image). Never commit broken code.

9. **Document Every Change.** Update `docs/CHANGELOG.md` after every significant commit. No silent changes.

10. **Batch Size = 1. Always.** Batch sizes > 1 will cause OOM on 2 GB VRAM. Hardcode `batch_size=1` wherever applicable. This is not configurable.

---

## 3. Workflow: The Phase Loop

Every phase from the [Master Plan](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md) must follow this exact 8-step loop:

```text
┌──────────────────────────────────────────────────────────┐
│                    THE PHASE LOOP                        │
│                                                          │
│  ① Pick Task ─► ② Plan ─► ③ Review Plan ─►              │
│  ④ Execute (Code) ─► ⑤ Review Execution ─►              │
│  ⑥ Test ─► ⑦ Fix / Improve ─► ⑧ Review & Commit        │
│       │                                                  │
│       └──── Update CHANGELOG.md ◄────────────────────    │
└──────────────────────────────────────────────────────────┘
```

| Step | Action | Owner |
|---|---|---|
| ① Pick Task | Select the next task from the current Phase's plan file | Developer + Agent |
| ② Plan | Agent proposes implementation approach, data flow, file changes | Agent |
| ③ Review Plan | Developer reviews and approves/rejects the approach | Developer |
| ④ Execute | Agent writes code following all constraints in this document | Agent |
| ⑤ Review Execution | Developer reviews code for correctness and constraint compliance | Developer |
| ⑥ Test | Run manual or automated tests; Agent provides test instructions | Agent + Developer |
| ⑦ Fix / Improve | If tests fail, Agent fixes issues. Loop back to ⑥ until green | Agent |
| ⑧ Review & Commit | Commit code + update `docs/CHANGELOG.md` | Developer + Agent |

---

## 4. Project Architecture (Folder Tree)

This folder structure is **non-negotiable**. Agents must always read from and write to the correct directories.

```text
ImageGeneratedAI/
├── AGENTS.md                    # THIS FILE — Project Constitution
├── README.md                    # Public-facing project overview
├── requirements.txt             # Python dependencies (pinned versions)
├── app.py                       # Gradio UI entrypoint
│
├── docs/                        # All documentation
│   ├── brief.md                 # Project vision (natural language)
│   ├── BRD.md                   # Business Requirements Document (FR, NFR, constraints)
│   ├── data-dictionary.md       # Data structure definitions (TBD)
│   ├── CHANGELOG.md             # Mandatory change log
│   ├── skills/                  # Custom agent skills
│   └── plans/                   # Phase-specific plans
│       ├── master-plan.md       # Central Kanban — Phase status tracker
│       ├── 01-crawl-data.md
│       ├── 02-preprocessing.md
│       ├── 03-finetune-lora.md
│       ├── 04-inference-pipeline.md
│       ├── 05-gradio-ui.md
│       ├── 06-review-optimize.md
│       └── 07-deploy.md
│
├── src/                         # Core inference modules
│   ├── segmentation.py          # U²-Net wrapper (CPU-first)
│   ├── inpaint.py               # SD 1.5 Inpainting + LoRA loader
│   ├── pipeline.py              # Orchestrator: seg → free GPU → inpaint → free GPU
│   ├── config.py                # Centralized configuration (paths, defaults)
│   └── utils.py                 # Shared utilities (image I/O, logging)
│
├── scripts/                     # Utility & automation scripts
│   ├── check_system.py          # Hardware detection script
│   ├── crawl_unsplash.py        # Unsplash API crawler
│   ├── crawl_pexels.py          # Pexels API crawler
│   ├── filter_person.py         # YOLO person filter
│   ├── segment_clothing.py      # Batch segmentation (U²-Net)
│   ├── generate_captions.py     # BLIP / manual captioning
│   ├── preprocess_images.py     # Resize, normalize, validate
│   ├── train_lora.py            # LoRA training script
│   ├── evaluate_lora.py         # LoRA evaluation on test images
│   └── benchmark_vram.py        # VRAM profiler (nvidia-smi)
│
├── data/                        # Strictly local data — NEVER commit to Git
│   ├── raw/                     # Raw crawled images + metadata.json
│   ├── processed/               # 512x512 images + masks/ + captions/
│   └── _rejected/               # Filtered-out images (no person detected)
│
├── models/                      # LoRA adapters — NEVER commit NSFW weights
│   ├── lora_fashion.safetensors
│   ├── lora_nsfw.safetensors
│   └── training_logs/
│
├── outputs/                     # Inference results — NEVER commit
│
├── tests/                       # Unit and integration tests (pytest)
│
└── notebooks/                   # Jupyter notebooks for exploration
```

### .gitignore Rules

The following directories must **never** be committed to version control:
- `data/` (contains images — too large, potentially NSFW)
- `models/` (contains model weights — too large, potentially NSFW)
- `outputs/` (contains generated images — potentially NSFW)
- `notebooks/` (exploration only, not production)
- `system_specs.json` (machine-specific)

---

## 5. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Language** | Python 3.10+ | Ecosystem compatibility with PyTorch, Diffusers |
| **ML Framework** | PyTorch | Industry standard, CUDA support |
| **Diffusion** | `diffusers` (HuggingFace) | SD 1.5 Inpainting pipeline, LoRA loading |
| **LoRA** | `peft` | Adapter management, merge/unmerge |
| **Attention** | `xformers` | Memory-efficient attention (~20% VRAM reduction) |
| **Segmentation** | U²-Net | Lightweight (~4 MB), runs well on CPU |
| **Image Processing** | `opencv-python-headless` | Headless variant — no GUI dependencies |
| **UI** | `gradio` | Local web UI, no frontend framework needed |
| **Base Model** | `runwayml/stable-diffusion-v1-5` | Lightest SD model that still produces acceptable quality (~1.7 GB fp16) |

### Prohibited Technologies

| Technology | Reason |
|---|---|
| SDXL, SD 2.x, SD 3.x, Flux | Exceeds 2 GB VRAM |
| ControlNet (full) | Adds ~2 GB on top of SD |
| IP-Adapter | Requires 3-4 GB VRAM |
| Any cloud inference API | Violates Offline-Only principle |
| TensorFlow | Unnecessary complexity; PyTorch is the standard |

---

## 6. Code Standards & Style

### General Rules
- **Type Hints**: Use type hints for **all** function signatures. No untyped public functions.
- **Docstrings**: Use Google-style docstrings for all public methods and classes.
- **Formatting**: Follow PEP 8. Line length ≤ 120 characters.
- **Imports**: Group imports in order: stdlib → third-party → local. Use absolute imports.
- **Dependencies**: Always prefer lightweight libraries (e.g., `opencv-python-headless` over `opencv-python`).

### VRAM-Critical Code Patterns

Every function that touches the GPU **must** follow this pattern:

```python
def run_inference(image: np.ndarray, prompt: str) -> np.ndarray:
    """Run SD 1.5 inpainting with LoRA.
    
    Args:
        image: Input image as numpy array (H, W, 3).
        prompt: Text prompt describing desired output.
        
    Returns:
        Generated image as numpy array (H, W, 3).
    """
    try:
        pipeline = load_pipeline()  # Load to GPU (fp16)
        pipeline.enable_attention_slicing()
        pipeline.enable_sequential_cpu_offload()
        
        result = pipeline(prompt=prompt, image=image, ...)
        return result
    finally:
        # MANDATORY: Always free GPU memory
        del pipeline
        torch.cuda.empty_cache()
        gc.collect()
```

---

## 7. Testing Protocol

### Unit Tests
- Location: `tests/` directory.
- Framework: `pytest`.
- Coverage target: 100% for utility functions (`src/utils.py`).
- Naming convention: `test_<module>_<function>.py`.

### Integration Tests
- Before marking any Phase as `Completed`, run the full pipeline on at least **one test image**.
- Verify: no OOM crash, output image is valid, VRAM peak ≤ 1.8 GB.

### Failure Protocol
1. If a test fails, the Agent **must** attempt to fix the issue before committing.
2. If the fix requires architectural changes, update the relevant plan file first, get Developer approval, then proceed.
3. Never commit code that fails tests.

---

## 8. Version Control & Changelog

### Commit Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore, perf
Scope: crawl, preprocess, lora, pipeline, ui, config, etc.

Examples:
  feat(crawl): add Unsplash API crawler with retry logic
  fix(pipeline): resolve VRAM overflow in inpainting step
  docs(changelog): update CHANGELOG for Phase 1 completion
  perf(pipeline): reduce inference time by disabling safety_checker
```

### Changelog Rules
- **MANDATORY**: Update `docs/CHANGELOG.md` after every significant commit.
- Format: `[YYYY-MM-DD] - <Brief description of change>`
- Group entries by date. Most recent at top within each date section.

---

## 9. VRAM Budget Allocation

This is the hard budget for every inference run. Agents must **never** exceed these limits.

```text
┌─────────────────────────────────────────────┐
│          VRAM BUDGET (2048 MiB total)        │
├─────────────────────────────────────────────┤
│  OS / Driver overhead        ~200 MiB       │
│  ─────────────────────────────────────────── │
│  Available for AI            ~1848 MiB       │
│  ─────────────────────────────────────────── │
│  SD 1.5 UNet (fp16)         ~1600 MiB       │
│  VAE Decoder (fp16)          ~100 MiB       │
│  LoRA Adapter                 ~50 MiB       │
│  Working memory               ~98 MiB       │
│  ─────────────────────────────────────────── │
│  HARD LIMIT                  1848 MiB       │
│  SOFT TARGET                 1800 MiB       │
└─────────────────────────────────────────────┘

⚠️  Segmentation (U²-Net) runs on CPU.
⚠️  SD pipeline must be fully unloaded before
    loading any other model on GPU.
```

---

## 10. LLM Role Assignment (Multi-Agent Strategy)

To optimize cost and quality, use different models for different task types:

| Task Type | Recommended Models | Rationale |
|---|---|---|
| **Strategic / Architecture** | Claude Opus 4.6, Gemini Pro 3.1 | Deep reasoning, system design, complex decisions |
| **Complex Code** (Pipeline, Training, Optimization) | Claude Sonnet 4.6, Gemini Flash 3.5 (High) | High accuracy, strong code generation |
| **Boilerplate / Crawlers / Tests** | Gemini Flash 3.5 (Low), Gemini Flash 3.1 | Fast, cheap, sufficient for routine tasks |
| **NSFW Content / Sensitive Prompts** | GPT-OSS (uncensored) | Bypasses strict content filters |
| **Documentation / Planning** | Any available model | Low complexity, any model works |

---

## 11. Phase Status Reference

Current project status (synced from [master-plan.md](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md)):

| Phase | Name | Status |
|---|---|---|
| Phase 0 | Setup & Documentation | ✅ Completed |
| Phase 1 | Data Crawling & Collection | 🟡 Ready to Start |
| Phase 2 | Preprocessing & Dataset | ⏳ Pending |
| Phase 3 | LoRA Fine-tuning | ⏳ Pending |
| Phase 4 | Inference Pipeline | ⏳ Pending |
| Phase 5 | Gradio UI | ⏳ Pending |
| Phase 6 | Review & Optimization | ⏳ Pending |
| Phase 7 | Packaging & Deploy | ⏳ Optional |

> **Next action**: Install Python 3.10+, create virtualenv, then begin Phase 1.

---

## 12. Quick Reference Card

```text
┌──────────────────────── AGENT QUICK REFERENCE ────────────────────────┐
│                                                                       │
│  ✅ DO:                          ❌ DON'T:                            │
│  • Use SD 1.5 + LoRA             • Use SDXL / SD3 / Flux             │
│  • Use fp16 everywhere           • Use fp32 (wastes VRAM)             │
│  • Batch size = 1                • Batch size > 1                     │
│  • CPU for segmentation          • GPU for segmentation               │
│  • empty_cache() after pipeline  • Leave models loaded                │
│  • Run offline                   • Call external APIs for inference   │
│  • Update CHANGELOG              • Make silent commits               │
│  • Test before commit            • Commit untested code              │
│  • LoRA rank ≤ 32                • LoRA rank > 32                    │
│  • Keep NSFW local               • Push NSFW to public repos         │
│                                                                       │
│  VRAM HARD LIMIT: 1.8 GB (1848 MiB)                                 │
│  INFERENCE TARGET: ≤ 120 seconds per 512x512 image                   │
│  BASE MODEL: runwayml/stable-diffusion-v1-5                          │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```
