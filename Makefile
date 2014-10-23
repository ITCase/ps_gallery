all: test

test:
	nosetests --with-coverage --cover-package pyramid_sacrud_gallery --cover-erase --with-doctest --nocapture

coverage: test
	coverage html
