PY=$(wildcard *.py)
JS=$(patsubst %.py, %.js, $(PY))
MINJS=$(patsubst %.py, %.min.js, $(PY))
CSS=$(patsubst %.scss, %.css, $(wildcard *.scss))

.SUFFIXES:

.SUFFIXES:
%.js: %.py
	./py2js compile $<
%.min.js: %.js
	./py2js minimize $<
%.css: %.scss
	env/bin/pysass $< $@

all: $(JS) $(MINJS) $(CSS)

whenevery-something-changes:
	bash -c 'while :; do inotifywait *.py; make all; done'

re: clean all

clean:
	rm -f $(JS) $(MINJS) $(CSS)
