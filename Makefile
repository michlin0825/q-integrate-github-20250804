.PHONY: help install run test demo clean lint

help:
	@echo "Available commands:"
	@echo "  install    Install dependencies"
	@echo "  run        Run the Flask application"
	@echo "  test       Run the test suite"
	@echo "  demo       Run the API demo (requires server to be running)"
	@echo "  clean      Clean up Python cache files"
	@echo "  lint       Run code linting (requires flake8)"

install:
	pip install -r requirements.txt

run:
	python app.py

test:
	pytest test_app.py -v

demo:
	python demo.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

lint:
	flake8 app.py test_app.py config.py demo.py --max-line-length=100