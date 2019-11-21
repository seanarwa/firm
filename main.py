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
pp = pprint.PrettyPrinter(indent=2)
camera = None

def signal_handler(sig, frame):
	log.info('Gracefully shutting down FIRM ...')
	if camera != None:
		camera.release()
	cv.destroyAllWindows()
	sys.exit(0)

def getProcessedFrame(frame):
	original_image = frame
	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	frame_gray = cv.equalizeHist(frame_gray)
	faces = config.face_cascade.detectMultiScale(
		frame_gray,
		scaleFactor=1.4,
		minNeighbors=1,
		minSize=(30,30)
	)
	for (x,y,w,h) in faces:
		center = (x + w//2, y + h//2)
		faceROI = frame_gray[y:y+h,x:x+w]
		eyes = config.eyes_cascade.detectMultiScale(faceROI)
		noses = config.nose_cascade.detectMultiScale(faceROI)
		mouths = config.mouth_cascade.detectMultiScale(faceROI)
		if (len(eyes) == 2):
			ts = str(time.time())
			log.info("matched: " + ts)
			cropped_img = original_image[y:y+h, x:x+w]
			cv.imwrite(os.path.join(DATA_DIR, ts + ".png"), cropped_img)
		if(config.draw_face):
			frame = cv.rectangle(frame, (x-10,y-10), (x+w+10,y+h+10), (255, 0, 255), thickness=2)
			for (x2,y2,w2,h2) in eyes:
				frame = cv.line(frame, (x + x2, y + y2 + h2//2), (x + x2 + w2, y + y2 + h2//2), (255, 0, 0), thickness=2)
			for (x2,y2,w2,h2) in noses:
				frame = cv.circle(frame, (x + x2 + w2//2, y + y2 + h2//2), 5, (255, 0, 0), thickness=cv.FILLED)
			for (x2,y2,w2,h2) in mouths:
				frame = cv.line(frame, (x + x2, y + y2 + h2//2), (x + x2 + w2, y + y2 + h2//2), (255, 0, 0), thickness=2)
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
			os.kill(os.getpid(), signal.SIGINT)

def main():
	
	signal.signal(signal.SIGINT, signal_handler)

	parser = argparse.ArgumentParser(description='Entrypoint script for face-identity-registry-matching')
	parser.add_argument('-f','--config_file', help='Path to configuration file.', default='config/config.yaml')
	parser.add_argument('-c','--clear_data', help='Option to clear data.', action='store_true')
	args = parser.parse_args()
	
	config.setLogging(log.INFO)
	config.load(args.config_file)
	
	if args.clear_data:
		log.info("Clearing data ...")
		shutil.rmtree(DATA_DIR, ignore_errors=True)
		log.info("Data directory deleted.\n")
		os.mkdir(DATA_DIR)
	else:
		os.makedirs(DATA_DIR, exist_ok=True)
	
	start_webcam()

if __name__ == "__main__":
	main()