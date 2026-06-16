# Master Plan - AI Fashion Editor

> Tài liệu quản lý dự án trung tâm — bảng điều khiển Kanban để Developer và AI Agent phối hợp nhịp nhàng.
> Tham chiếu: [brief.md](file:///e:/ImageGeneratedAI/docs/brief.md) · [BRD.md](file:///e:/ImageGeneratedAI/docs/BRD.md) · [AGENTS.md](file:///e:/ImageGeneratedAI/AGENTS.md)

---

## 1. Mục tiêu chiến lược (Strategic Goals)

| # | Mục tiêu | Đo lường thành công |
|---|---|---|
| **G1** | Xây dựng dataset chất lượng ~500 ảnh phụ nữ Việt Nam/Đông Á kèm caption và mask | ≥ 500 ảnh raw, ≥ 300 ảnh processed với mask + caption |
| **G2** | Fine-tune LoRA ổn định trên Stable Diffusion 1.5 cho 2 mục đích: thay trang phục + NSFW | ≥ 2 file `.safetensors` hoạt động, loss hội tụ |
| **G3** | Chạy inference local trên GPU MX330 (2GB VRAM) với latency khả dụng | ≤ 120 giây/ảnh 512x512, peak VRAM ≤ 1.8 GB, 0 OOM crash |
| **G4** | Giao diện Gradio hoàn chỉnh, 100% offline, bảo mật tuyệt đối | UI functional, ngắt internet vẫn chạy, không telemetry |

---

## 2. Quy trình làm việc (Workflow Rule)

*Nhắc lại từ [AGENTS.md](file:///e:/ImageGeneratedAI/AGENTS.md):*

Mỗi Phase sẽ đi qua vòng lặp:

```text
Plan → Code → Review → Test → Commit
  │                              │
  └──── Cập nhật CHANGELOG.md ◄──┘
```

- **Plan**: AI Agent đọc plan của phase hiện tại, xác nhận scope với Developer.
- **Code**: Viết code, tuân thủ ràng buộc VRAM (xem BRD mục 6).
- **Review**: Developer review code, AI Agent sửa theo feedback.
- **Test**: Chạy kiểm thử thủ công theo hướng dẫn AI Agent cung cấp.
- **Commit**: Commit code + cập nhật `docs/CHANGELOG.md`.

---

## 3. Danh sách các Phase chi tiết (PHASE MASTER TABLE)

| Phase | Mục tiêu (Goal) | Nhiệm vụ chính (Key Tasks) | Đầu ra (Deliverables) | Trạng thái (Status) | Phụ thuộc (Depends on) |
|:---|:---|:---|:---|:---|:---|
| **Phase 0** | Thiết lập hiến pháp & docs | ① Tạo `AGENTS.md` quy định hiến pháp AI Agent ② Viết `docs/brief.md` tổng quan dự án ③ Viết `docs/BRD.md` đặc tả yêu cầu chi tiết (FR, NFR, constraints) ④ Tạo cấu trúc thư mục (`docs/`, `src/`, `scripts/`, `data/`) ⑤ Tạo `scripts/check_system.py` kiểm tra hardware | [AGENTS.md](file:///e:/ImageGeneratedAI/AGENTS.md), [brief.md](file:///e:/ImageGeneratedAI/docs/brief.md), [BRD.md](file:///e:/ImageGeneratedAI/docs/BRD.md), [master-plan.md](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md), [check_system.py](file:///e:/ImageGeneratedAI/scripts/check_system.py) | ✅ `Completed` | — |
| **Phase 1** | Thu thập dữ liệu (Crawl & Collect) | ① Viết `scripts/crawl_unsplash.py` dùng Unsplash API (retry 3 lần khi fail, sleep random 1-3s giữa requests) ② Viết `scripts/crawl_pexels.py` dùng Pexels API (tương tự logic retry) ③ Viết `scripts/filter_person.py` dùng YOLO để lọc ảnh có người (confidence ≥ 0.7) ④ Tạo metadata JSON cho mỗi ảnh (`filename`, `source`, `resolution`, `has_person`) ⑤ Dự phòng: script download từ Kaggle dataset nếu API bị rate-limit | `data/raw/*.jpg`, `data/raw/metadata.json`, `scripts/crawl_*.py`, `scripts/filter_person.py` | 🟡 `In Progress` | Phase 0 |
| **Phase 2** | Tiền xử lý & Tạo dataset | ① Viết `scripts/segment_clothing.py` — dùng U²-Net tạo mask vùng trang phục (chạy trên **CPU** hoặc GPU khi rảnh) ② Viết `scripts/generate_captions.py` — dùng BLIP hoặc viết caption thủ công cho ≥ 100 ảnh ③ Viết `scripts/preprocess_images.py` — resize về 512x512, chuẩn hóa RGB, lọc ảnh lỗi ④ Tổ chức dataset theo cấu trúc thư mục chuẩn cho LoRA training | `data/processed/*.png`, `data/processed/masks/*.png`, `data/processed/captions/*.txt`, `scripts/segment_clothing.py`, `scripts/generate_captions.py`, `scripts/preprocess_images.py` | ⏳ `Pending` | Phase 1 |
| **Phase 3** | Fine-tune LoRA | ① Viết `scripts/train_lora.py` — config LoRA rank=32, fp16, batch_size=1, learning_rate=1e-4 ② Train LoRA "fashion" cho thay trang phục (có thể dùng Google Colab / RunPod nếu local quá chậm) ③ Train LoRA "nsfw" cho xóa trang phục ④ Viết `scripts/evaluate_lora.py` — test LoRA trên 10 ảnh sample, so sánh output ⑤ Log loss curves và lưu checkpoints | `models/lora_fashion.safetensors`, `models/lora_nsfw.safetensors`, `scripts/train_lora.py`, `scripts/evaluate_lora.py`, `models/training_logs/` | ⏳ `Pending` | Phase 2 |
| **Phase 4** | Xây dựng Pipeline Inference | ① Viết `src/pipeline.py` — tích hợp SD 1.5 Inpainting + LoRA loading, fp16, attention slicing, sequential CPU offload ② Viết `src/segmentation.py` — wrapper U²-Net cho runtime (load → segment → **unload khỏi GPU** → trả mask) ③ Viết `src/inference.py` — orchestrator: gọi segmentation → giải phóng GPU → gọi inpainting → giải phóng GPU ④ Viết `scripts/benchmark_vram.py` — đo peak VRAM bằng `nvidia-smi`, assert ≤ 1.8 GB ⑤ Test end-to-end: 10 ảnh liên tiếp không OOM | `src/pipeline.py`, `src/segmentation.py`, `src/inference.py`, `scripts/benchmark_vram.py`, `data/test_outputs/` | ⏳ `Pending` | Phase 3 |
| **Phase 5** | Xây dựng Giao diện UI | ① Viết `src/app.py` — Gradio app với các tab: Upload ảnh, Vẽ/chỉnh mask (brush tool), Nhập prompt + cấu hình (CFG, steps, seed), NSFW toggle, Hiển thị before/after, Download kết quả ② Viết `src/config.py` — quản lý settings (model path, LoRA path, default params) ③ Tích hợp pipeline inference vào UI ④ Test UX: upload → mask → prompt → result → export | `src/app.py`, `src/config.py` | ⏳ `Pending` | Phase 4 |
| **Phase 6** | Review & Tối ưu | ① Profiling toàn pipeline bằng `scripts/benchmark_vram.py` — ghi nhận bottleneck ② Kiểm thử edge cases: ảnh rộng (landscape), ảnh tối, ảnh nhiều người, ảnh không có người ③ Tối ưu latency: thử `safety_checker=None`, xformers, VAE slicing ④ Code refactor: thêm docstring, comment, error handling ⑤ Viết báo cáo hiệu suất `docs/performance_report.md` | `docs/performance_report.md`, code refactored | ⏳ `Pending` | Phase 5 |
| **Phase 7** *(Tùy chọn)* | Packaging & Deploy | ① Tạo `Dockerfile` hoặc script đóng gói `.exe` (PyInstaller) ② Viết `README.md` hướng dẫn cài đặt và sử dụng ③ Tạo `requirements.txt` cuối cùng ④ Test trên máy sạch (clean install) | `Dockerfile` hoặc `installer/`, `README.md`, `requirements.txt` | ⏳ `Optional` | Phase 6 |

---

## 4. Lịch trình dự kiến (Timeline Estimation)

```text
Phase 0 ████████████████████ Completed (Ngày 1)
Phase 1 ░░░░░░░░░░░░░░░░░░░ 2 ngày   (crawl + filter, chờ API)
Phase 2 ░░░░░░░░░░░░░░       1 ngày   (segmentation + caption + resize)
Phase 3 ░░░░░░░░░░░░░░░░░░░ 1-2 ngày (train LoRA, có thể chạy overnight)
Phase 4 ░░░░░░░░░░░░░░░░░░░ 1.5 ngày (pipeline + benchmark)
Phase 5 ░░░░░░░░░░░░░░       1 ngày   (Gradio UI)
Phase 6 ░░░░░░░░░░░░░░       1 ngày   (profiling + refactor)
Phase 7 ░░░░░░░░             0.5 ngày (packaging, tùy chọn)
        ─────────────────────────────
        Tổng ước tính: ~8-10 ngày (tùy tốc độ phối hợp Developer + Agent)
```

---

## 5. Rủi ro & Giải pháp (Risks & Mitigations)

| # | Rủi ro | Mức nghiêm trọng | Giải pháp (Mitigation) |
|---|---|---|---|
| **R1** | Unsplash/Pexels rate-limit chặn IP khi crawl | 🟡 Trung bình | Dùng `time.sleep(random.uniform(1, 3))` giữa requests. Dự phòng: download dataset có sẵn từ Kaggle (`fashion-image-dataset`, `person-detection`). |
| **R2** | Train LoRA bị OOM trên local GPU (2 GB VRAM) | 🔴 Cao | Chuyển training lên **Google Colab** (miễn phí, T4 16GB) hoặc **RunPod** (~$0.5/h). Chỉ copy file `.safetensors` về local để inference. |
| **R3** | Train LoRA bị OOM trên Colab miễn phí (session bị ngắt) | 🟡 Trung bình | Giảm batch size về 1, giảm resolution về 512x512. Fallback: RunPod pay-as-you-go. Lưu checkpoint mỗi 200 steps. |
| **R4** | Inference quá chậm trên MX330 (>120 giây) | 🟡 Trung bình | Giảm inference steps (20→15), dùng `safety_checker=None` (tiết kiệm ~1s), bật xformers, giảm resolution nếu cần. |
| **R5** | U²-Net segmentation không chính xác trên ảnh phức tạp | 🟡 Trung bình | Cho phép chỉnh mask thủ công trên Gradio (FR-03). Thử thay bằng `rembg` hoặc SAM (Segment Anything) lite nếu U²-Net quá kém. |
| **R6** | **GPU bị dùng sai chỗ** — Load đồng thời Segmentation + SD | 🔴 Cao | **Chiến lược cứng: CPU cho Segmentation, GPU chỉ cho SD Inpainting**. Trong code phải đảm bảo `torch.cuda.empty_cache()` + `del model` trước khi chuyển pipeline. AI Agent tuyệt đối không được load 2 model cùng lúc trên GPU. |
| **R7** | Python chưa cài trên máy (đã xác nhận) | 🟢 Thấp | Cài Python 3.10/3.11 + pip trước khi bắt đầu Phase 1. Tạo virtualenv riêng cho dự án. |

---

## 6. Checklist nghiệm thu toàn dự án (Final Acceptance)

- [ ] **Dataset**: ≥ 500 ảnh raw, ≥ 300 ảnh processed với mask + caption.
- [ ] **LoRA**: Ít nhất 2 file LoRA (fashion + NSFW) load được vào SD 1.5 không lỗi.
- [ ] **Thay trang phục**: AI thay được áo dài/đầm/váy trên ảnh người thật, kết quả tự nhiên trên ≥ 8/10 ảnh test.
- [ ] **Xóa trang phục**: NSFW toggle hoạt động, xóa quần áo tái tạo cơ thể tự nhiên trên ≥ 8/10 ảnh test.
- [ ] **VRAM**: Peak VRAM ≤ 1.8 GB, 0 OOM crash trong 20 ảnh liên tiếp.
- [ ] **Latency**: Inference ≤ 120 giây/ảnh 512x512 (20 steps).
- [ ] **Offline**: Ngắt internet → toàn bộ pipeline vẫn chạy bình thường.
- [ ] **Bảo mật**: Không gửi ảnh ra internet, không telemetry, không log cloud.
- [ ] **UI**: Gradio khởi động ≤ 30s, tất cả chức năng (upload/mask/prompt/NSFW/export) đều functional.
- [ ] **Code quality**: Toàn bộ code có comment và docstring, theo chuẩn PEP 8.

---

## 7. Kế hoạch chi tiết từng Phase

Mỗi Phase sẽ có file plan riêng trong `docs/plans/`:

| Phase | File plan | Trạng thái |
|---|---|---|
| Phase 1 | [01-crawl-data.md](file:///e:/ImageGeneratedAI/docs/plans/01-crawl-data.md) | 📄 Skeleton (chờ fill) |
| Phase 2 | [02-preprocessing.md](file:///e:/ImageGeneratedAI/docs/plans/02-preprocessing.md) | 📄 Skeleton (chờ fill) |
| Phase 3 | [03-finetune-lora.md](file:///e:/ImageGeneratedAI/docs/plans/03-finetune-lora.md) | 📄 Skeleton (chờ fill) |
| Phase 4 | [04-inference-pipeline.md](file:///e:/ImageGeneratedAI/docs/plans/04-inference-pipeline.md) | 📄 Skeleton (chờ fill) |
| Phase 5 | [05-gradio-ui.md](file:///e:/ImageGeneratedAI/docs/plans/05-gradio-ui.md) | 📄 Skeleton (chờ fill) |
| Phase 6 | [06-review-optimize.md](file:///e:/ImageGeneratedAI/docs/plans/06-review-optimize.md) | 📄 Skeleton (chờ fill) |
| Phase 7 | [07-deploy.md](file:///e:/ImageGeneratedAI/docs/plans/07-deploy.md) | 📄 Skeleton (chờ fill) |
