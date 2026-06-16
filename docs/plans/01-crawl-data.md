# Phase 1: Thu thập dữ liệu (Crawl & Collect)

> **Trạng thái**: 🟡 In Progress
> **Phụ thuộc**: Phase 0 (✅ Completed)
> **Tham chiếu**: [master-plan.md](file:///e:/ImageGeneratedAI/docs/plans/master-plan.md) · [BRD.md](file:///e:/ImageGeneratedAI/docs/BRD.md)

---

## Mục tiêu
Thu thập ≥ 500 ảnh phụ nữ Việt Nam / Đông Á chất lượng cao từ các nguồn hợp pháp.

## Nhiệm vụ
- [x] Viết `scripts/crawl_unsplash.py` (Unsplash API, retry 3 lần, sleep random 1-3s, support NSFW flag)
- [x] Viết `scripts/crawl_pexels.py` (Pexels API, logic tương tự)
- [x] Viết `scripts/crawl_kaggle.py` (Kaggle fallback dataset utility)
- [x] Viết `scripts/filter_person.py` (YOLO filter, confidence ≥ 0.7)
- [x] Tạo `data/raw/metadata.json` (filename, source, resolution, has_person)
- [x] Cấu hình thư mục và keywords cho NSFW crawling (`data/raw/nsfw/`)
- [ ] Phân phối API Keys / Cài đặt môi trường Python 3.10+
- [ ] Chạy crawl thử nghiệm (Smoke test) và YOLO filter
- [ ] Chạy crawl toàn bộ và xử lý bộ lọc ảnh

## Đầu ra
- `data/raw/*.jpg`
- `data/raw/metadata.json`
- `scripts/crawl_*.py`
- `scripts/filter_person.py`

## Tiêu chí nghiệm thu
- [ ] ≥ 500 ảnh raw đã download
- [ ] ≥ 80% ảnh có người (sau khi filter)
- [ ] Metadata JSON đầy đủ cho mỗi ảnh

