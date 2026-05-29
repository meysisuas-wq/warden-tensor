help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
install:	pip install -r requirements.txt
dev:	uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload
test:	pytest tests/ -v --cov=src
lint:	black src/ tests/ && isort src/ tests/ && ruff check src/ tests/
docker-up:	docker-compose up -d
docker-down:	docker-compose down
clean:	find . -type d -name __pycache__ -exec rm -rf {} +
