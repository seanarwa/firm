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

DATA_DIR = "data"
pp = pprint.PrettyPrinter(indent=2)
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
nose_cascade = cv.CascadeClassifier()
mouth_cascade = cv.CascadeClassifier()
camera_port = 0
draw_face = False
camera = None

def signal_handler(sig, frame):
	print('Gracefully shutting down FIRM ...')
	if camera != None:
		camera.release()
	cv.destroyAllWindows()
	sys.exit(0)

def getProcessedFrame(frame):
	original_image = frame
	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	frame_gray = cv.equalizeHist(frame_gray)
	faces = face_cascade.detectMultiScale(
		frame_gray,
		scaleFactor=1.4,
		minNeighbors=1,
		minSize=(30,30)
	)
	for (x,y,w,h) in faces:
		center = (x + w//2, y + h//2)
		faceROI = frame_gray[y:y+h,x:x+w]
		eyes = eyes_cascade.detectMultiScale(faceROI)
		noses = nose_cascade.detectMultiScale(faceROI)
		mouths = mouth_cascade.detectMultiScale(faceROI)
		if (len(eyes) == 2):
			ts = str(time.time())
			print("matched: " + ts)
			cropped_img = original_image[y:y+h, x:x+w]
			cv.imwrite(os.path.join(DATA_DIR, ts + ".png"), cropped_img)
		if(draw_face):
			frame = cv.rectangle(frame, (x-10,y-10), (x+w+10,y+h+10), (255, 0, 255), thickness=2)
			for (x2,y2,w2,h2) in eyes:
				frame = cv.line(frame, (x + x2, y + y2 + h2//2), (x + x2 + w2, y + y2 + h2//2), (255, 0, 0), thickness=2)
			for (x2,y2,w2,h2) in noses:
				frame = cv.circle(frame, (x + x2 + w2//2, y + y2 + h2//2), 5, (255, 0, 0), thickness=cv.FILLED)
			for (x2,y2,w2,h2) in mouths:
				frame = cv.line(frame, (x + x2, y + y2 + h2//2), (x + x2 + w2, y + y2 + h2//2), (255, 0, 0), thickness=2)
	return frame
	
def loadConfig(config_file_name):
	print("Loading config ...")
	
	loaded_config = None
	with open(config_file_name, "r") as config_file:
		try:
			loaded_config = yaml.safe_load(config_file) 	
		except yaml.YAMLError as e:
			print(e)
			
	face_cascade_path = os.path.join("config", loaded_config["face_cascade_file"])
	eyes_cascade_path = os.path.join("config", loaded_config["eyes_cascade_file"])
	nose_cascade_path = os.path.join("config", loaded_config["nose_cascade_file"])
	mouth_cascade_path = os.path.join("config", loaded_config["mouth_cascade_file"])
	
	if not face_cascade.load(cv.samples.findFile(face_cascade_path)):
		print('ERROR: loading face cascade')
		exit(0)
	
	if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_path)):
		print('ERROR: loading eyes cascade')
		exit(0)
		
	if not nose_cascade.load(cv.samples.findFile(nose_cascade_path)):
		print('ERROR: loading nose cascade')
		exit(0)
		
	if not mouth_cascade.load(cv.samples.findFile(mouth_cascade_path)):
		print('ERROR: loading mouth cascade')
		exit(0)
	
	camera_port = int(loaded_config["camera_port"])
	draw_face = bool(loaded_config["draw_face"])
	
	pp.pprint(loaded_config)
	print("Config loading complete.\n")

def start_webcam():
	print("Starting webcam ...")
	camera = cv.VideoCapture(camera_port, cv.CAP_DSHOW)
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

	print(cv.utils)
	
	signal.signal(signal.SIGINT, signal_handler)

	parser = argparse.ArgumentParser(description='Entrypoint script for face-identity-registry-matching')
	parser.add_argument('-f','--config_file', help='Path to configuration file.', default='config/config.yaml')
	parser.add_argument('-c','--clean', help='Option to clear data.', action='store_true')
	args = parser.parse_args()
	
	loadConfig(args.config_file)
	
	if args.clean:
		print("Clearing data ...")
		shutil.rmtree(DATA_DIR, ignore_errors=True)
		print("Data directory deleted.\n")
		
	os.makedirs(DATA_DIR, exist_ok=True)
	
	start_webcam()

if __name__ == "__main__":
	main()