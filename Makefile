install:
	pip install -r requirements.txt

run:
	python manage.py runserver 0.0.0.0:8000

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

clear-cache:
	python manage.py clear_cache

free-port:
	fuser -k -n tcp 8000
