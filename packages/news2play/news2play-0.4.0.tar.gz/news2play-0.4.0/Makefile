.PHONY: init publish clean

IMAGE = deep3/news2play:latest

init: Pipfile
	pip3 install pipenv --upgrade
	pipenv install --dev
publish:
	rm -rf build dist .eggs *.egg-info

	pip3 install 'twine>=1.5.0'
	python3 setup.py publish

	rm -rf build dist .eggs *.egg-info
clean:
	rm -rf build dist .eggs *.egg-info
docker_build:
    docker build -t $(IMAGE) .
docker_push:
	docker push $(IMAGE)
docker_run:
	docker run -it -p 5000:5000 $(IMAGE)

