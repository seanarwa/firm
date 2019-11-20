from __future__ import print_function
import cv2 as cv
import argparse
import time
import os

DATA_DIR = "data/"
os.mkdir(DATA_DIR)
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
camera = 0

def getFace(frame):
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
		frame = cv.rectangle(frame, (x-10,y-10), (x+w+10,y+h+10), (255, 0, 255), thickness=2)
		faceROI = frame_gray[y:y+h,x:x+w]
		eyes = eyes_cascade.detectMultiScale(faceROI)
		if (len(eyes) == 2):
			ts = str(time.time())
			print("matched: " + ts)
			img_name = ts + ".png"
			cv.imwrite(DATA_DIR + img_name, frame)
		for (x2,y2,w2,h2) in eyes:
			# eye_center = (x + x2 + w2//2, y + y2 + h2//2)
			# radius = int(round((w2 + h2)*0.25))
			# frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
			frame = cv.line(frame, (x + x2, y + y2 + h2//2), (x + x2 + w2, y + y2 + h2//2), (255, 0, 0), thickness=2)
	return frame
	
def loadConfig(fc, ec, c):
	print("Loading config ...")
	if not face_cascade.load(cv.samples.findFile(str(fc))):
		print('ERROR: loading face cascade')
		exit(0)
	print("CONFIG: face_cascade = %s" % (fc))
	if not eyes_cascade.load(cv.samples.findFile(str(ec))):
		print('ERROR: loading eyes cascade')
		exit(0)
	print("CONFIG: eyes_cascade = %s" % (ec))
	camera = int(c)
	print("CONFIG: camera = %s" % (c))
	print("Config loading complete.\n")

def start_webcam():
	print("Starting webcam ...")
	cam = cv.VideoCapture(0)
	while True:
		ret, frame = cam.read()
		if frame is None:
			break
		frame = cv.flip(frame, 1)
		frame = getFace(frame)
		cv.imshow('webcam', frame)
		if cv.waitKey(1) == 27: 
			break  # esc to quit
	cv.destroyAllWindows()

def main():
	parser = argparse.ArgumentParser(description='Entrypoint script for face-identity-registry')
	parser.add_argument('--face_cascade', help='Path to face cascade.', default='config/haarcascade_frontalface_default.xml')
	parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='config/haarcascade_eye_tree_eyeglasses.xml')
	parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
	args = parser.parse_args()
	
	loadConfig(args.face_cascade, args.eyes_cascade, args.camera)

	start_webcam()

if __name__ == "__main__":
	main()