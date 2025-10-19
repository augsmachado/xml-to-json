# virtual environment commands
venv-create:
	python3 -m venv venv

venv-up:
	source venv/bin/activate

venv-down:
	deactivate

# python commands
install-pip:
	pip install --upgrade pip
	pip install -r requirements.txt --upgrade

freeze-pip:
	pip freeze > requirements.txt

# tests commands
run-tests:
	pytest tests --disable-warnings

# fastapi commands
run-fastapi:
	uvicorn main:app --reload