all :
	true

pylint :
	pylint --rcfile=pylint.ini \
		ulib \
		*.py \
		--output-format=colorized 2>&1 | less -SR

clean :
	find . -type f -name '*.pyc' -exec rm '{}' \;
	rm -rf pkg-root.arch pkg src build ulib.egg-info

