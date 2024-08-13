.PHONY: install
install:
	pip install -r requirements.txt
	
.PHONY: runserver
runserver:
	python manage.py runserver

.PHONY: make_migrations
make_migrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: createsuperuser
createsuperuser:
	python manage.py createsuperuser