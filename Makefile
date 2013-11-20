all :
	true

pylint :
	pylint --rcfile=pylint.ini \
		ulib \
		*.py \
		--output-format=colorized 2>&1 | less -SR

clean :
	find . -type d -name '__pycache__' -exec rm -rf '{}' \;
	rm -rf pkg-root.arch pkg src build ulib.egg-info

