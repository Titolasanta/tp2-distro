SHELL := /bin/bash
PWD := $(shell pwd)

GIT_REMOTE = github.com/7574-sistemas-distribuidos/docker-compose-init

default: build

all:

deps:
	go mod tidy
	go mod vendor

build: deps
	GOOS=linux go build -o bin/client github.com/7574-sistemas-distribuidos/docker-compose-init/client
.PHONY: build


docker-compose-up: 
	docker-compose -f docker.fake up --build --remove-orphans
.PHONY: docker-compose-up

docker-compose-down:
	docker-compose -f docker.fake stop -t 1
	docker-compose -f docker.fake down
.PHONY: docker-compose-down

docker-compose-setup:
	docker run -d --rm --name dummy -v myvolume:/root alpine tail -f /dev/null
	docker cp ./yelp_academic_dataset_business.json dummy:/root
	docker cp ./yelp_academic_dataset_review.json dummy:/root
	docker stop dummy
.PHONY:docker-compose-setup

docker-compose-clean:
	docker volume rm myvolume
.PHONY:docker-compose-clean

docker-compose-logs:
	docker-compose -f docker-compose-dev.yaml logs -f
.PHONY: docker-compose-logs
