# Phase 4: Xây dựng Pipeline Inference

> **Trạng thái**: ⏳ Pending
> **Phụ thuộc**: Phase 3
> **Tham chiếu**: [master-plan.md](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md) · [BRD.md mục 5 & 6](file:///e:/ImageGeneratedAI/docs/BRD.md)

---

## Mục tiêu
Tích hợp SD 1.5 + LoRA + Inpainting, tối ưu VRAM ≤ 1.8 GB, 0 OOM crash.

## Nhiệm vụ
- [ ] Viết `src/pipeline.py` (SD 1.5 Inpainting + LoRA, fp16, attention slicing, CPU offload)
- [ ] Viết `src/segmentation.py` (U²-Net wrapper: load → segment → unload GPU → trả mask)
- [ ] Viết `src/inference.py` (orchestrator: segmentation → giải phóng GPU → inpainting → giải phóng GPU)
- [ ] Viết `scripts/benchmark_vram.py` (đo peak VRAM, assert ≤ 1.8 GB)
- [ ] Test end-to-end: 10 ảnh liên tiếp không OOM

## Đầu ra
- `src/pipeline.py`
- `src/segmentation.py`
- `src/inference.py`
- `scripts/benchmark_vram.py`
- `data/test_outputs/`

---

*Chi tiết sẽ được điền khi Phase 4 bắt đầu triển khai.*
