# Phase 2: Tiền xử lý & Tạo dataset

> **Trạng thái**: ⏳ Pending
> **Phụ thuộc**: Phase 1
> **Tham chiếu**: [master-plan.md](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md)

---

## Mục tiêu
Xử lý ảnh raw thành dataset chuẩn cho LoRA training (512x512, mask, caption).

## Nhiệm vụ
- [ ] Viết `scripts/segment_clothing.py` (U²-Net, chạy trên CPU)
- [ ] Viết `scripts/generate_captions.py` (BLIP hoặc caption thủ công)
- [ ] Viết `scripts/preprocess_images.py` (resize 512x512, chuẩn hóa RGB)
- [ ] Tổ chức dataset theo cấu trúc chuẩn LoRA training

## Đầu ra
- `data/processed/*.png`
- `data/processed/masks/*.png`
- `data/processed/captions/*.txt`

---

*Chi tiết sẽ được điền khi Phase 2 bắt đầu triển khai.*
