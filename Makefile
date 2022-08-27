.PHONY: run docker test

# APP
run:
	uvicorn app.main:app

run.debug:
	uvicorn app.main:app --reload

# DOCKER
docker.build:
	docker build -t fastapi .
docker.compose.up:
	docker-compose -f ./docker-compose-dev.yml up
docker.compose.down:
	docker-compose -f ./docker-compose-dev.yml down
docker.push:
	docker push aliakram/fastapi

# TESTING
test:
	pytest -v -s