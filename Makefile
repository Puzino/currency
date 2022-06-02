SHELL := /bin/bash

manage_py := python app/manage.py

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

run:
	$(manage_py) runserver

worker:
	cd app && celery -A settings worker -l info

beat:
	cd app && celery -A settings beat -l info

pytest:
	pytest ./app/tests --cov=app --cov-report html -vv && coverage report --fail-under=50
