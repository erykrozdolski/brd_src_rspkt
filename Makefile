SASS = sass --scss

SCSS = $(PWD)/web/sass
CSS = $(PWD)/web/static/css

compile:
	$(SASS) --watch --scss $(SCSS):$(CSS)
run:
	    python $(PWD)/manage.py runserver
migrate:
	    python $(PWD)/manage.py migrate
migrations:
	    python $(PWD)/manage.py makemigrations

watch:
    $(SASS) --watch --scss $(SCSS):$(CSS)
    $(SASS) sass/main.scss:$(CSS)/main.css


