# python commands
py-install:
	pip install --upgrade pip
	pip install -r requirements.txt --upgrade

py-run-tests:
	pytest tests

# fastapi commands
fastapi-run:
	uvicorn main:app --reload