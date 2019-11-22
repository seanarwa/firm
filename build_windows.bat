@echo off

pip --version

pip install -r requirements.txt
pyinstaller main.py
XCOPY /E config dist\main\config\