#!/bin/bash

python3 -m venv pa1
source pa1/bin/activate
pip3 install -r requirements.txt

python3 main.py -s seeds-2020100953.txt -n 1000