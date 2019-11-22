from __future__ import print_function
import cv2 as cv
import argparse
import time
import os
import yaml
import pprint
import shutil
import signal
import sys
import logging as log

# local modules
import config

DATA_DIR = "data"
camera = None

def print_banner(app_version):
	spaced_text = " FIRM " + str(app_version) + " "
	banner = spaced_text.center(78, '=')
	print(banner)

def graceful_shutdown():
	log.info('Gracefully shutting down FIRM ...')
	if camera != None:
		camera.release()
	cv.destroyAllWindows()
	sys.exit(0)

def signal_handler(sig, frame):
	graceful_shutdown()

def getProcessedFrame(frame):
	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	frame_gray = cv.equalizeHist(frame_gray)
	faces = config.face_cascade.detectMultiScale(
		frame_gray,
		scaleFactor=1.4,
		minNeighbors=1,
		minSize=(30,30)
	)
	for (x,y,w,h) in faces:
		faceROI = frame_gray[y:y+h,x:x+w]
		eyes = config.eyes_cascade.detectMultiScale(faceROI)
		noses = config.nose_cascade.detectMultiScale(faceROI)
		mouths = config.mouth_cascade.detectMultiScale(faceROI)
		if(config.draw_enabled):
			if(config.draw_face):
				frame = cv.rectangle(frame, (x-10,y-10), (x+w+10,y+h+10), (255, 0, 255), thickness=2)
			if(config.draw_eyes):
				for (x2,y2,w2,h2) in eyes:
					frame = cv.line(frame, (x + x2, y + y2 + h2//2), (x + x2 + w2, y + y2 + h2//2), (255, 0, 0), thickness=2)
			if(config.draw_nose):
				for (x2,y2,w2,h2) in noses:
					frame = cv.circle(frame, (x + x2 + w2//2, y + y2 + h2//2), 5, (255, 0, 0), thickness=cv.FILLED)
			if(config.draw_mouth):
				for (x2,y2,w2,h2) in mouths:
					frame = cv.line(frame, (x + x2, y + y2 + h2//2), (x + x2 + w2, y + y2 + h2//2), (255, 0, 0), thickness=2)
		if (len(eyes) == 2):
			ts = str(time.time())
			path = os.path.join(DATA_DIR, str(int(config.PROGRAM_START_TIMESTAMP)), ts + ".png")
			log.info("matched: " + path)
			cropped_img = frame[y:y+h, x:x+w]
			cv.imwrite(path, cropped_img)
	return frame

def start_webcam():
	log.info("Starting webcam ...")
	camera = cv.VideoCapture(config.camera_port, cv.CAP_DSHOW)
	while True:
		ret, frame = camera.read()
		if not ret:
			continue
		frame = cv.flip(frame, 1)
		frame = getProcessedFrame(frame)
		cv.imshow('webcam', frame)
		if cv.waitKey(1) == 27:
			graceful_shutdown()
	return

def main():
	
	signal.signal(signal.SIGINT, signal_handler)

	parser = argparse.ArgumentParser(description='Entrypoint script for face-identity-registry-matching (FIRM)')
	parser.add_argument('-f','--config_file', help='Path to configuration file.', default='config/app.yaml')
	args = parser.parse_args()
	
	config.load(args.config_file)

	print_banner(config.app_version)
	
	os.makedirs(os.path.join(DATA_DIR, str(int(config.PROGRAM_START_TIMESTAMP))), exist_ok=True)
	
	start_webcam()

if __name__ == "__main__":
	main()