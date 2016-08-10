.PHONY: clean lint requirements

#################################################################################
# COMMANDS                                                                      #
#################################################################################

requirements:
	# pip install -q -r requirements.txt

clean:
	find . -name "*.pyc" -exec rm {} \;

lint:
	flake8 --exclude=lib/,bin/ .

build_model_iris: requirements
	python ml_src/build_model_iris.py

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
