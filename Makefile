.PHONY: run build docker

run:
	uvicorn app.main:app

run.debug:
	uvicorn app.main:app --reload

build:
	docker build -t fastapi .

docker.compose.up:
	docker-compose -f ./docker-compose-dev.yml up
docker.compose.down:
	docker-compose -f ./docker-compose-dev.yml down
docker.push:
	docker push aliakram/fastapi