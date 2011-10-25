build:
	virtualenv --no-site-packages env
	. env/bin/activate
	pip install -r requirements.txt

clean:
	find . -name '*~' -o -name '*.pyc' -print0 | xargs -0 -r rm

check:
	trial influx

lint: pep8 pyflakes

pep8:
	pep8 `find influx/ -name \*py`

pyflakes:
	pyflakes `find influx/ -name \*py`
