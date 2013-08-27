bin:
	virtualenv -p python2.7 .

bin/nosetests: bin
	bin/pip install nose nose-cov
	
test: bin/nosetests
	bin/nosetests --with-coverage --cover-erase --cover-package addonreg addonreg 

clean:
	rm -rf bin lib local include man

doc:
	bin/pip install mozilla-sphinx-theme sphinx
	cd docs && make html

