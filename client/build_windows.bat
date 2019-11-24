@echo off

pip --version

pip install -r requirements.txt
pyinstaller main.py
XCOPY /E config dist\main\config\
XCOPY /E config\dlib\face_recognition_models dist\main\face_recognition_models\