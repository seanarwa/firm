import logging as log
import yaml
import os
import cv2 as cv
import pprint
import sys
import time

face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
nose_cascade = cv.CascadeClassifier()
mouth_cascade = cv.CascadeClassifier()
camera_port = 0
draw_face = False

pp = pprint.PrettyPrinter(indent=2)

PROGRAM_START_TIMESTAMP=time.time()

def setLogging(log_level="INFO", log_file="app.log", log_timestamp=True):

	if (log_level == "DEBUG"):
		log_level = log.DEBUG
	elif (log_level == "INFO"):
		log_level = log.INFO
	elif (log_level == "WARNING"):
		log_level = log.WARNING
	elif (log_level == "ERROR"):
		log_level = log.ERROR
	elif (log_level == "CRITICAL"):
		log_level = log.CRITICAL
	else:
		print("ERROR: invalid log level was specified log_level=" + str(log_level))
		exit(0)

	root = log.getLogger()
	root.setLevel(log_level)
	formatter = log.Formatter('%(asctime)s - %(levelname)s: %(message)s')

	streamHandler = log.StreamHandler(sys.stdout)
	streamHandler.setLevel(log_level)
	streamHandler.setFormatter(formatter)
	root.addHandler(streamHandler)

	if(log_timestamp):
		index = log_file.rfind(".")
		log_file = log_file[:index] + "." + str(int(PROGRAM_START_TIMESTAMP)) + log_file[index:]

	log_file_path = os.path.join("config", log_file)
	os.makedirs("log", exist_ok=True)
	fileHandler = log.FileHandler(log_file_path)
	fileHandler.setLevel(log_level)
	fileHandler.setFormatter(formatter)
	root.addHandler(fileHandler)
	
	return

def load(config_file_name):
	
	loaded_config = None
	with open(config_file_name, "r") as config_file:
		try:
			loaded_config = yaml.safe_load(config_file)
		except yaml.YAMLError as e:
			log.error(e)

	logging_config = loaded_config["logging"]
	log_level = str(logging_config["level"])
	log_file = str(logging_config["file"])
	log_timestamp = bool(logging_config["timestamp"])
	setLogging(log_level, log_file, log_timestamp)

	log.info("Loading config ...")
	
	algorithm_config = loaded_config["algorithm"]
	face_cascade_path = os.path.join("config", algorithm_config["face_cascade_file"])
	eyes_cascade_path = os.path.join("config", algorithm_config["eyes_cascade_file"])
	nose_cascade_path = os.path.join("config", algorithm_config["nose_cascade_file"])
	mouth_cascade_path = os.path.join("config", algorithm_config["mouth_cascade_file"])
	
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
	
	log.info("\n" + pp.pformat(loaded_config))
	log.info("Config loading complete.\n")
	
	return