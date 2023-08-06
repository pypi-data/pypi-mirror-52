#!/bin/bash

#Update source file
DIRECTORY=/build/lbciagent
mkdir -p $DIRECTORY
if [ ! -d "$DIRECTORY/virtualenv" ]; then
	echo "Creating new enviroment"
    virtualenv $DIRECTORY/virtualenv
	source $DIRECTORY/virtualenv/bin/activate
	pip install pika
	pip install --extra-index-url https://lbmultipython03.cern.ch/simple/ --trusted-host lbmultipython03.cern.ch lbmessaging
	pip install --extra-index-url https://lbmultipython03.cern.ch/simple/ --trusted-host lbmultipython03.cern.ch lbciagent
fi
