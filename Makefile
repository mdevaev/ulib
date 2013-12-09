all :
	true

pylint :
	pylint --rcfile=pylint.ini \
		ulib \
		*.py \
		--output-format=colorized 2>&1 | less -SR

clean :
	find . -type f -name '*.py?' -delete
	find . -type d -name __pycache__ -delete
	rm -rf pkg-root.arch pkg src build ulib.egg-info

