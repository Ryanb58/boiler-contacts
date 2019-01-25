build:
	docker build --tag=contacts .

tag:
	docker tag contacts:latest ryanb58/boiler-contacts:latest

push:
	docker push ryanb58/boiler-contacts:latest

