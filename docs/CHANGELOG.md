# CHANGELOG

Nhật ký ghi nhận toàn bộ các thay đổi và nâng cấp của dự án **AI Fashion Assistant**.

Format ghi nhận: `[YYYY-MM-DD] - <Mô tả ngắn gọn thay đổi>`

---

## [2026-06-16]
- Khởi tạo cấu trúc thư mục dự án ban đầu.
- Tạo file [AGENTS.md](file:///e:/ImageGeneratedAI/AGENTS.md) quy định hiến pháp hoạt động cho AI Agent.
- Tạo cấu trúc thư mục tài liệu `docs/` gồm: `brief.md`, `BRD.md`, `plans/master-plan.md`, `CHANGELOG.md`.
- [Documentation] - Viết brief.md tổng quan dự án.
- [Documentation] - Viết lại brief.md với góc nhìn storytelling, gần gũi hơn.
- [Documentation] - Hoàn thiện BRD đặc tả hệ thống dựa trên cấu hình hardware thực tế.
- [Documentation] - Xây dựng master-plan tổng thể, phân chia 7 Phase chi tiết.
- [Documentation] - Tạo skeleton plan cho Phase 1-7 (`docs/plans/01-*.md` → `07-*.md`).
- [Documentation] - Reworked AGENTS.md into an English, comprehensive project constitution.
- [Chore] - Set up project ecosystem including Cursor rules (`.cursor/rules/`), GitHub issue and PR templates, GitHub Actions CI workflow, and pre-commit hooks configuration.
- [Chore] - Added Makefile for task execution and development utilities (install, lint, test, crawl, train, ui, clean).
- [Documentation] - Created phase-specific skills documentation files in `docs/skills/` (Phase 1 to 5).
- [Chore] - Set up `pyproject.toml` configuration, updated `.env.example`, and created cross-platform environment installers (`setup.sh` and `setup.bat`).
- [Feat] - Completed Phase 1 plan and created crawl and filter scripts: `src/config.py`, `src/utils.py`, `scripts/crawl_unsplash.py`, `scripts/crawl_pexels.py`, `scripts/crawl_kaggle.py`, `scripts/filter_person.py`, and unit tests `tests/test_utils.py`.
- [Feat] - Added NSFW crawling options to Unsplash script, configured NSFW directories, isolated data under `data/raw/nsfw`, and added comprehensive unit test verification.

