.PHONY: lint pep8 pyflakes clean

lint: pep8 pyflakes

pep8:
	pep8 --repeat import.py
	pep8 `find influx/ -name \*py`

pyflakes:
	pyflakes import.py
	pyflakes `find influx/ -name \*py`

clean:
	find . -name '*~' -o -name '*.pyc' -print0 | xargs -0 -r rm

check:
	trial influx
