.PHONY: test run clean build npm-install pip-install

test:
	python -m unittest

run:
	export FLASK_ENV=development
	export FLASK_DEBUG=1
	python manage.py run

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf doku/static/dist
	rm -rf doku/static/node_modules

build:
	cd doku/static && npm run build

npm-install:
	cd doku/static && npm install

pip-install:
	pip install -r requirements.txt
