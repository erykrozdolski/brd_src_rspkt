SASS = sass --scss

SCSS = $(PWD)/sass
CSS = $(PWD)/web/static/css

migrate:
	    python $(PWD)/manage.py migrate
migrations:
	    python $(PWD)/manage.py makemigrations
watch:
	$(DEFAULT_RUN) grunt watch

run:
	python $(PWD)/manage.py runserver

run_for_ext:
	$(DEFAULT_RUN) "$(PWD)/manage.py runserver 0.0.0.0:8000"


