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

test:
	@$(MANAGE) test

user_fixture:
	@$(MANAGE) dumpdata users.User --indent 4 >> users.json

i18n_makemessages_ru:
	poetry run django-admin makemessages -l ru

i18n_compilemessages:
	poetry run django-admin compilemessages
