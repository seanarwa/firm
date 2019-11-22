import cv2 as cv
import argparse
import time
import os
import signal
import sys
import logging as log

# local modules
import config
import face_detection

camera = None

def print_banner(app_version):
	spaced_text = " FIRM " + str(app_version) + " "
	banner = spaced_text.center(78, '=')
	print(banner)

def graceful_shutdown():
	log.info('Gracefully shutting down FIRM ...')
	if camera != None:
		camera.stop()
		camera.release()
	cv.destroyAllWindows()
	sys.exit(0)

def signal_handler(sig, frame):
	graceful_shutdown()

def start_webcam():
	log.info("Starting webcam ...")
	camera = cv.VideoCapture(config.camera_port, cv.CAP_DSHOW)
	while True:
		ret, frame = camera.read()
		if not ret:
			continue
		frame = cv.flip(frame, 1)
		frame = face_detection.get_caffemodel_processed_frame(frame)
		cv.imshow(config.app_name + " " + config.app_version, frame)
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
	
	os.makedirs(os.path.join(config.DATA_DIR, str(int(config.PROGRAM_START_TIMESTAMP))), exist_ok=True)
	
	start_webcam()

if __name__ == "__main__":
	main()