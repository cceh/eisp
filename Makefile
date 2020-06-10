.PHONY: clean install image
default: clean install

clean:
	rm -fr \
		__pycache__ \
		build \
		dist \
		eisp.egg-info \
		eisp/docs/*.html
install:
	pip3 install -r requirements.txt
	python3 setup.py install
image:
	docker build -t cceh/eisp:0.0.1 .
