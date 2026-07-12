.PHONY: up down build rebuild logs

up:
	docker compose up

down:
	docker compose down

build:
	docker compose build

rebuild:
	docker compose build --no-cache

logs:
	docker compose logs -f

rabbitmq:
	docker run -it --rm --name rabbitmq \
		-p 5672:5672 \
		-p 15672:15672 \
		--env-file .env \
		-v "${CURDIR}/config/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf:ro" \
		rabbitmq:4-management

sync:
	uv sync --all-extras --dev
