# AI Fashion Editor - Business Requirements Document (BRD)

> Tài liệu đặc tả yêu cầu chi tiết cho dự án **AI Fashion Editor**.
> Tham chiếu: [brief.md](file:///e:/ImageGeneratedAI/docs/brief.md) · [master-plan.md](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md) · [AGENTS.md](file:///e:/ImageGeneratedAI/AGENTS.md)

---

## 1. Giới thiệu (Introduction)

### 1.1 Mục đích
Tài liệu này đặc tả toàn bộ yêu cầu chức năng, phi chức năng, luồng xử lý và ràng buộc kỹ thuật cho dự án **AI Fashion Editor** — một ứng dụng AI chạy hoàn toàn local, cho phép nhận diện, thay thế và xóa trang phục trên ảnh người thật.

### 1.2 Phạm vi
- **Trong phạm vi**: Crawl dữ liệu, tiền xử lý ảnh, fine-tune LoRA, pipeline inference (thay/xóa quần áo), giao diện Gradio UI.
- **Ngoài phạm vi**: Text-to-Image tạo người từ văn bản, xử lý video, cloud deployment, multi-user SaaS, mobile app.

### 1.3 Cấu hình phần cứng tham chiếu
Mọi quyết định kiến trúc trong tài liệu này đều dựa trên cấu hình thực tế:

| Thành phần | Thông số |
|---|---|
| **Máy** | Acer Aspire 3 |
| **CPU** | Intel(R) Core(TM) i5-1035G1 @ 1.00GHz (4C/8T, Ice Lake) |
| **RAM** | 7.8 GB DDR4 |
| **GPU (CUDA)** | NVIDIA GeForce MX330 — **2048 MiB (2 GB VRAM)** |
| **CUDA Compute** | 6.1 (hỗ trợ fp16) |
| **OS** | Windows 11 Home |

---

## 2. Các bên liên quan (Stakeholders)

| Vai trò | Mô tả | Trách nhiệm |
|---|---|---|
| **Người dùng (End User)** | Chủ dự án, sử dụng trực tiếp trên máy local | Upload ảnh, chọn chế độ, nhập prompt, đánh giá kết quả |
| **AI Agent (Cursor/Claude)** | Trợ lý lập trình AI | Viết code, tối ưu hóa, đề xuất giải pháp tuân thủ AGENTS.md |
| **Developer** | Người điều phối dự án | Review code, kiểm thử thủ công, quyết định kiến trúc |

---

## 3. Yêu cầu chức năng (Functional Requirements)

| ID | Tên | Mô tả | Ưu tiên |
|---|---|---|---|
| **FR-01** | Upload ảnh | Người dùng upload ảnh đầu vào (JPG/PNG, tối đa 2048x2048). Hệ thống tự động resize về 512x512 trước khi xử lý để phù hợp VRAM. | Cao |
| **FR-02** | Segmentation tự động | Sử dụng U²-Net để tạo mask phân đoạn vùng trang phục (áo, quần, váy, đầm) và vùng cơ thể. Chạy trên CPU hoặc GPU tùy tải. | Cao |
| **FR-03** | Chỉnh mask thủ công | Cho phép người dùng vẽ lại, mở rộng hoặc thu hẹp mask trên giao diện Gradio (brush tool). | Trung bình |
| **FR-04** | Inpainting thay trang phục | Người dùng nhập prompt mô tả trang phục mong muốn (ví dụ: *"Áo dài trắng"*). Hệ thống dùng SD 1.5 Inpainting + LoRA để vẽ lại vùng mask. | Cao |
| **FR-05** | Inpainting xóa trang phục (NSFW) | Xóa lớp trang phục và tái tạo vùng cơ thể ẩn bên dưới. Sử dụng LoRA NSFW chuyên biệt. | Cao |
| **FR-06** | NSFW Toggle | Nút bật/tắt chế độ NSFW trên UI. Khi tắt, tính năng xóa trang phục bị ẩn hoàn toàn. | Trung bình |
| **FR-07** | Cấu hình prompt nâng cao | Cho phép chỉnh: negative prompt, guidance scale (CFG), số bước inference (steps), seed. | Thấp |
| **FR-08** | Export kết quả | Tải ảnh kết quả về máy (PNG, chất lượng gốc). Hỗ trợ so sánh before/after trên UI. | Trung bình |
| **FR-09** | Quản lý LoRA | Cho phép chọn/chuyển đổi giữa các file LoRA khác nhau (ví dụ: LoRA áo dài, LoRA NSFW, LoRA Hàn Quốc). | Thấp |

---

## 4. Yêu cầu phi chức năng (Non-Functional Requirements)

> **Do giới hạn 2GB VRAM**, tất cả các yêu cầu phi chức năng bên dưới đều được thiết kế xoay quanh việc tối ưu hóa tài nguyên phần cứng cực đoan.

| ID | Danh mục | Yêu cầu | Ngưỡng |
|---|---|---|---|
| **NFR-01** | Performance | Thời gian inference 1 ảnh 512x512 (20 steps) | ≤ 120 giây |
| **NFR-02** | Performance | Thời gian segmentation 1 ảnh | ≤ 10 giây |
| **NFR-03** | Memory (VRAM) | Peak VRAM sử dụng trong mọi pipeline | ≤ 1.8 GB (dự phòng 200 MB cho OS/driver) |
| **NFR-04** | Memory (VRAM) | Tuyệt đối không load đồng thời 2 model trên GPU | 0 model song song |
| **NFR-05** | Memory (RAM) | Peak RAM sử dụng cho AI pipeline | ≤ 5 GB (dành ~3 GB cho OS + apps) |
| **NFR-06** | Privacy | Không gọi API bên ngoài, không gửi dữ liệu qua mạng | 100% offline |
| **NFR-07** | Privacy | Không có telemetry, analytics hay tracking | Zero telemetry |
| **NFR-08** | Privacy | Dữ liệu NSFW chỉ lưu local, không đồng bộ cloud | Local-only storage |
| **NFR-09** | Usability | Giao diện Gradio khởi động và sẵn sàng sử dụng | ≤ 30 giây |
| **NFR-10** | Stability | Không crash do OOM (Out of Memory) trong quá trình inference | 0 OOM crash |

---

## 5. Luồng xử lý (System Workflow)

```text
┌─────────────────────────────────────────────────────────────────┐
│                    LUỒNG XỬ LÝ CHÍNH                           │
└─────────────────────────────────────────────────────────────────┘

[Người dùng]
    │
    ▼
(1) Upload ảnh đầu vào (JPG/PNG)
    │
    ▼
(2) Tiền xử lý ────────────────────────────────────────────────┐
    │  • Resize về 512x512                                      │
    │  • Chuẩn hóa màu sắc (OpenCV)                            │
    │                                                           │
    ▼                                                           │
(3) Segmentation (U²-Net) ──── [Chạy trên GPU hoặc CPU]        │
    │  • Tạo mask vùng trang phục                               │
    │  • Output: mask image (đen/trắng)                         │
    │                                                           │
    ▼                                                           │
(4) ⚠️ GIẢI PHÓNG GPU ─────── torch.cuda.empty_cache()         │
    │  • Unload U²-Net khỏi VRAM                               │
    │  • Đảm bảo VRAM trống trước khi load SD                  │
    │                                                           │
    ▼                                                           │
(5) Người dùng chỉnh mask (tùy chọn, trên Gradio)              │
    │                                                           │
    ▼                                                           │
(6) Chọn chế độ: ──────────────────────────────────────┐        │
    │                                                   │        │
    ├─ [A] Thay trang phục ──► Nhập prompt              │        │
    │                          + Load LoRA phù hợp      │        │
    │                                                   │        │
    └─ [B] Xóa trang phục ──► NSFW toggle ON            │        │
                               + Load LoRA NSFW         │        │
    │                                                   │        │
    ▼                                                   │        │
(7) Inpainting (SD 1.5 + LoRA) ─── [fp16, attention     │        │
    │  slicing, CPU offload]                             │        │
    │  • Input: ảnh gốc + mask + prompt                  │        │
    │  • Output: ảnh kết quả                             │        │
    │                                                   │        │
    ▼                                                   │        │
(8) ⚠️ GIẢI PHÓNG GPU ─────── torch.cuda.empty_cache()  │        │
    │                                                   │        │
    ▼                                                   │        │
(9) Hiển thị kết quả (before/after) trên Gradio         │        │
    │                                                   │        │
    ▼                                                   │        │
(10) Export ảnh kết quả (PNG)                            │        │
    └───────────────────────────────────────────────────┘        │
                                                                 │
    ⚡ LƯU Ý QUAN TRỌNG:                                        │
    Bước (4) và (8) là BẮT BUỘC để đảm bảo không vượt 1.8GB    │
    VRAM tại bất kỳ thời điểm nào.                              │
    └────────────────────────────────────────────────────────────┘
```

---

## 6. Ràng buộc kỹ thuật (Technical Constraints)

> **Do giới hạn 2GB VRAM**, các ràng buộc kỹ thuật bên dưới là **bắt buộc, không thương lượng**.

### 6.1 Base Model

| Thuộc tính | Giá trị | Lý do |
|---|---|---|
| **Model** | `runwayml/stable-diffusion-v1-5` | Model SD nhẹ nhất còn cho chất lượng tốt (~1.7 GB fp16) |
| **Variant** | Inpainting (`sd-v1-5-inpainting`) | Hỗ trợ mask-based editing out-of-the-box |
| **Precision** | `torch.float16` (fp16) | Giảm 50% VRAM so với fp32, GPU MX330 hỗ trợ (Compute 6.1) |

**CẤM sử dụng**: SDXL, SD 2.x, SD 3.x, Flux, DALL-E — tất cả đều vượt quá 2 GB VRAM.

### 6.2 Fine-tuning

| Thuộc tính | Giá trị | Lý do |
|---|---|---|
| **Phương pháp** | LoRA (Low-Rank Adaptation) | File LoRA chỉ 10-100 MB, không cần train toàn bộ model |
| **LoRA Rank** | ≤ 32 | Rank cao hơn tốn thêm VRAM khi inference, vượt ngưỡng 1.8 GB |
| **Precision** | Mixed precision fp16 | Bắt buộc cho cả training và inference |
| **Batch size** | **1** (cố định, CẤM > 1) | Batch size > 1 sẽ gây OOM trên 2 GB VRAM |

**CẤM sử dụng**: Full fine-tuning, DreamBooth full, Textual Inversion nặng.

### 6.3 Tối ưu hóa bộ nhớ (Bắt buộc áp dụng)

```text
pipeline.enable_attention_slicing()          # Giảm peak VRAM khi chạy attention
pipeline.enable_sequential_cpu_offload()     # Chuyển layer không dùng sang RAM
pipeline.enable_vae_slicing()                # Giảm VRAM khi decode VAE
torch.cuda.empty_cache()                     # Dọn VRAM fragments sau mỗi pipeline
```

### 6.4 Thư viện bắt buộc

| Thư viện | Vai trò |
|---|---|
| `diffusers` | Pipeline Stable Diffusion (inpainting, LoRA loading) |
| `peft` | LoRA adapter management |
| `xformers` | Memory-efficient attention (giảm thêm ~20% VRAM) |
| `gradio` | Web UI local |
| `opencv-python` | Tiền/hậu xử lý ảnh (resize, crop, color) |
| `torch` (PyTorch) | Backend tính toán GPU/CPU |

### 6.5 Segmentation & Tiền xử lý

| Thuộc tính | Giá trị |
|---|---|
| **Model segmentation** | U²-Net (~4 MB weights) |
| **Chạy trên** | GPU khi rảnh, fallback CPU (i5-1035G1) |
| **Quy tắc** | Phải unload U²-Net khỏi VRAM **trước** khi load SD 1.5 |

### 6.6 Không khả thi do VRAM

Các công nghệ sau **không thể sử dụng** trên cấu hình 2 GB VRAM:

| Công nghệ | VRAM tối thiểu | Trạng thái |
|---|---|---|
| SDXL | ~6 GB | ❌ Không khả thi |
| ControlNet (full) | ~4 GB (thêm ~2 GB trên SD) | ❌ Không khả thi |
| IP-Adapter | ~3-4 GB | ❌ Không khả thi |
| SD 3.x / Flux | ~8-12 GB | ❌ Không khả thi |
| Batch inference (batch > 1) | Nhân đôi VRAM | ❌ Không khả thi |

---

## 7. Use Cases (Ca sử dụng)

### Use Case 1: Thử áo dài ảo

| Mục | Chi tiết |
|---|---|
| **Actor** | Người dùng |
| **Precondition** | Có ảnh chụp chân dung/toàn thân phụ nữ Việt Nam |
| **Luồng chính** | Upload ảnh → AI segmentation tạo mask vùng áo → Người dùng xác nhận mask → Nhập prompt: *"Áo dài trắng truyền thống, thêu hoa sen"* → AI inpaint → Xem kết quả before/after → Export PNG |
| **Thời gian dự kiến** | 60-120 giây (inference) |
| **Output** | Ảnh 512x512 với áo dài thay thế |

### Use Case 2: Xóa nội y (NSFW Research)

| Mục | Chi tiết |
|---|---|
| **Actor** | Người dùng (riêng tư, local) |
| **Precondition** | Bật NSFW toggle, có LoRA NSFW đã train |
| **Luồng chính** | Upload ảnh → AI segmentation tạo mask toàn bộ trang phục → Chọn chế độ "Xóa trang phục" → AI inpaint tái tạo cơ thể → Xem kết quả → Export |
| **Ràng buộc** | 100% offline, không log, không gửi dữ liệu ra ngoài |
| **Output** | Ảnh 512x512 NSFW (lưu local-only) |

### Use Case 3: Train LoRA mới

| Mục | Chi tiết |
|---|---|
| **Actor** | Developer / Người dùng nâng cao |
| **Precondition** | Dataset đã crawl và tiền xử lý xong (Phase 1 + 2 hoàn thành) |
| **Luồng chính** | Chuẩn bị 50-200 ảnh + caption → Chạy script training LoRA (rank ≤ 32, fp16, batch=1) → Xuất file `.safetensors` → Load vào pipeline inference để test |
| **Ràng buộc** | Training trên GPU MX330 sẽ rất chậm (~vài giờ cho 1000 steps). Có thể cân nhắc train trên Google Colab rồi copy file LoRA về local |
| **Output** | File LoRA `.safetensors` (10-100 MB) |

---

## 8. Tiêu chí nghiệm thu (Acceptance Criteria)

### Checklist nghiệm thu tổng thể

| # | Tiêu chí | Điều kiện đạt | Phase liên quan |
|---|---|---|---|
| AC-01 | Dataset tối thiểu | ≥ 200 ảnh đã crawl, ≥ 100 ảnh đã gán caption | Phase 1 |
| AC-02 | Segmentation hoạt động | U²-Net tạo mask chính xác ≥ 80% vùng trang phục trên 20 ảnh test | Phase 2 |
| AC-03 | LoRA training thành công | File `.safetensors` được tạo, load vào pipeline không lỗi | Phase 3 |
| AC-04 | Inpainting thay trang phục | Ảnh output có trang phục mới khớp prompt, không artifacts nghiêm trọng trên 10/10 ảnh test | Phase 4 |
| AC-05 | Inpainting xóa trang phục | Ảnh output tái tạo cơ thể tự nhiên, không artifacts nghiêm trọng trên 10/10 ảnh test | Phase 4 |
| AC-06 | VRAM không vượt ngưỡng | Peak VRAM ≤ 1.8 GB trong suốt quá trình inference (đo bằng `nvidia-smi`) | Phase 4, 6 |
| AC-07 | Không OOM crash | Chạy 20 ảnh liên tiếp không crash do Out of Memory | Phase 6 |
| AC-08 | Inference time | ≤ 120 giây cho 1 ảnh 512x512, 20 steps | Phase 4, 6 |
| AC-09 | UI hoạt động | Gradio UI khởi động ≤ 30s, upload/mask/prompt/export đều functional | Phase 5 |
| AC-10 | 100% Offline | Ngắt internet → toàn bộ pipeline vẫn chạy bình thường | Tất cả |
