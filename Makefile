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
	@$(MANAGE) dumpdata users.User --pks 1 --indent 4 > ./task_manager/tests/fixtures/users.json

status_fixture:
	@$(MANAGE) dumpdata statuses.Status --pks 1 --indent 4 > ./task_manager/tests/fixtures/statuses.json

label_fixture:
	@$(MANAGE) dumpdata labels.Label --indent 4 > ./task_manager/tests/fixtures/labels.json

task_fixture:
	@$(MANAGE) dumpdata tasks.Task --indent 4 > ./task_manager/tests/fixtures/tasks.json

i18n_makemessages_ru:
	poetry run django-admin makemessages -l ru

i18n_compilemessages:
	poetry run django-admin compilemessages

lint:
	poetry run flake8 task_manager
