#!/bin/sh

pip --version

pip install -r requirements.txt
cython main.py --embed