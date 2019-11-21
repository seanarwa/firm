import logging as log
import yaml
import os
import cv2 as cv
import pprint as pp
import sys

face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
nose_cascade = cv.CascadeClassifier()
mouth_cascade = cv.CascadeClassifier()
camera_port = 0
draw_face = False

def setLogging(log_level):

	log.basicConfig(filename='app.log', level=log.INFO)

	root = log.getLogger()
	root.setLevel(log_level)

	handler = log.StreamHandler(sys.stdout)
	handler.setLevel(log_level)
	formatter = log.Formatter('%(asctime)s - %(levelname)s: %(message)s')
	handler.setFormatter(formatter)
	root.addHandler(handler)
	
	return

def load(config_file_name):
	log.info("Loading config ...")
	
	loaded_config = None
	with open(config_file_name, "r") as config_file:
		try:
			loaded_config = yaml.safe_load(config_file)
		except yaml.YAMLError as e:
			log.error(e)
			
	face_cascade_path = os.path.join("config", loaded_config["face_cascade_file"])
	eyes_cascade_path = os.path.join("config", loaded_config["eyes_cascade_file"])
	nose_cascade_path = os.path.join("config", loaded_config["nose_cascade_file"])
	mouth_cascade_path = os.path.join("config", loaded_config["mouth_cascade_file"])
	
	if not face_cascade.load(cv.samples.findFile(face_cascade_path)):
		log.error('cv cannot load face cascade file = ' + str(face_cascade_path))
		exit(0)
	
	if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_path)):
		log.error('cv cannot load eyes cascade file = ' + str(eyes_cascade_path))
		exit(0)
		
	if not nose_cascade.load(cv.samples.findFile(nose_cascade_path)):
		log.error('cv cannot load nose cascade file = ' + str(nose_cascade_path))
		exit(0)
		
	if not mouth_cascade.load(cv.samples.findFile(mouth_cascade_path)):
		log.error('cv cannot load mouth cascade file = ' + str(mouth_cascade_path))
		exit(0)
	
	camera_port = int(loaded_config["camera_port"])
	draw_face = bool(loaded_config["draw_face"])
	
	log.info(pp.pformat(loaded_config))
	log.info("Config loading complete.\n")
	
	return