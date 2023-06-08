MANAGE := poetry run python3 manage.py

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

makemigrations:
	@$(MANAGE) makemigrations

migrate:
	@$(MANAGE) migrate

runserver:
	@$(MANAGE) runserver

shell:
	@$(MANAGE) shell_plus --ipython
