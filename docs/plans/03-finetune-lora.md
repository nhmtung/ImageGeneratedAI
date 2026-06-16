# Phase 3: Fine-tune LoRA

> **Trạng thái**: ⏳ Pending
> **Phụ thuộc**: Phase 2
> **Tham chiếu**: [master-plan.md](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md) · [BRD.md mục 6.2](file:///e:/ImageGeneratedAI/docs/BRD.md)

---

## Mục tiêu
Train ≥ 2 LoRA adapters (fashion + NSFW) trên SD 1.5 với rank ≤ 32, fp16.

## Nhiệm vụ
- [ ] Viết `scripts/train_lora.py` (rank=32, fp16, batch=1, lr=1e-4)
- [ ] Train LoRA "fashion" (thay trang phục)
- [ ] Train LoRA "nsfw" (xóa trang phục)
- [ ] Viết `scripts/evaluate_lora.py` (test trên 10 ảnh sample)
- [ ] Log loss curves, lưu checkpoints mỗi 200 steps

## Đầu ra
- `models/lora_fashion.safetensors`
- `models/lora_nsfw.safetensors`
- `models/training_logs/`

---

*Chi tiết sẽ được điền khi Phase 3 bắt đầu triển khai.*
