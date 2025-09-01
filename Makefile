# ---------------- Virtual environment
create-venv:
	python3 -m venv venv

up-venv:
	source venv/bin/activate

down-venv:
	deactivate

# python commands
py-install:
	pip install --upgrade pip
	pip install -r requirements.txt --upgrade

py-run-tests:
	pytest tests

# fastapi commands
fastapi-run:
	uvicorn main:app --reload