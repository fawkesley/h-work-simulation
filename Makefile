.PHONY: test
test:
	nosetests -vs --stop

.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
