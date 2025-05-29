# Dev Containers make commands

build:
	docker compose up --build -d --remove-orphans

up:
	docker compose up -d

down:
	docker compose down

down-v:
	docker compose down -v

banker-config:
	docker compose config

makemigrations:
	docker compose run --rm api python manage.py makemigrations

migrate:
	docker compose run --rm api python manage.py migrate

collectstatic:
	docker compose run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose run --rm api python manage.py createsuperuser

flush:
	docker compose run --rm api python manage.py flush

network-inspect:
	docker network inspect banker_local_nw

banker-db:
	docker compose exec postgres bash -c "psql -U $$POSTGRES_USER -d $$POSTGRES_DB"

reset-containers:
	docker compose down -v --remove-orphans
	docker system prune --all --force --volumes
	docker network create banker_local_nw
	docker compose up --build -d --remove-orphans

run-test:
	docker compose run --rm api python manage.py test $(if $(app),$(app))
	docker compose down -v

clear-dev-containers:
	docker compose down


logs-api:
	docker compose logs api

# Runs Github Unittest Workflow Docker Compose Commands

gha-run-test:
	docker compose -f docker-compose.test.yml run --rm api_test python manage.py test

gha-down-test:
	docker compose -f docker-compose.test.yml down -v

gha-clear-test:
	docker compose -f docker-compose.test.yml down -v --remove-orphans
	docker system prune --all --force --volumes

gha-reset-test:
	docker compose -f docker-compose.test.yml down -v --remove-orphans
	docker system prune --all --force --volumes
	docker compose -f docker-compose.test.yml up --build -d --remove-orphans

