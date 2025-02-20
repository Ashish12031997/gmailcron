build:
	docker build -t gmail-api-backend .
	docker-compose build

start: build
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose run --rm test

migrate:
	python manage.py makemigrations mail_manager_backend
	python manage.py migrate

# Install all dependencies inside the Docker container
install:
	docker-compose run --rm web pip install --no-cache-dir -r requirements.txt

# Remove all containers, images, and volumes
clean: down
	docker system prune -f
	docker volume prune -f
	docker image prune -f

# Remove and reinstall all dependencies
reinstall: clean
	docker-compose up
	docker-compose run --rm web pip install --no-cache-dir -r requirements.txt

# Run database scripts (assuming a script located at ./scripts/init_db.py)
run-db-scripts:
	docker-compose run --rm web python scripts/init_db.py

delete-pycache:
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY:  build up down logs test install clean reinstall run-db-scripts delete-pycache
