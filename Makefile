.PHONY: install lint test crawl train ui clean

install:
	pip install -r requirements.txt
	pre-commit install

lint:
	black src/ scripts/ tests/
	isort src/ scripts/ tests/
	flake8 src/ scripts/ tests/ --max-line-length=120

test:
	pytest tests/ -v

crawl:
	python scripts/crawl_unsplash.py --limit 50
	python scripts/crawl_pexels.py --limit 50

train:
	python scripts/train_lora.py --config configs/train_config.yaml

ui:
	python app.py

clean:
	powershell -Command "Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force"
	powershell -Command "Get-ChildItem -Recurse -File -Filter '*.pyc' | Remove-Item -Force"
