#!/bin/bash

export $(cat .env | xargs)
export PYTHONPATH=$PYTHONPATH:$PROJ_PATH
source activate $VENV
