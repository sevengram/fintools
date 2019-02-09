#!/usr/bin/env bash

BASE_DIR=$1
source ${BASE_DIR}/venv/bin/activate
python3 ${BASE_DIR}/update_quote.py ${BASE_DIR}/configs/db.conf ${BASE_DIR}/configs/api.conf
