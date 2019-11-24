import os
import time
import logging as log
import cv2 as cv
import numpy as np
import face_recognition

# local modules
import config

def process(frame):

    if config.frame_resize_enabled:
        resize_scale = config.frame_resize_scale
        frame = cv.resize(frame, (0, 0), fx=resize_scale, fy=resize_scale)

    frames = [frame]
    
    layer_count = 1
    for extraction_layer in config.extraction_layers:

        if extraction_layer == "haarcascade":
            frames = extract_haarcascade_faces(frames)
        elif extraction_layer == "caffemodel":
            frames = extract_caffemodel_faces(frames)
        else:
            log.error("Unknown extraction layer: " + str(extraction_layer))
            exit(0)
        
        log.debug("Extraction layer %d - %s captured: %d" % (layer_count, extraction_layer, len(frames)))
        layer_count += 1

    for frame in frames:
        save_frame(frame)

def extract_haarcascade_faces(frames):

    results = []

    for frame in frames:

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.equalizeHist(frame_gray)
        faces = config.haarcascade_face_cascade.detectMultiScale(
            frame_gray,
            scaleFactor=1.4,
            minNeighbors=1,
            minSize=(30,30)
        )

        for (x,y,w,h) in faces:

            cropped_img = frame[y:y+h, x:x+w]
            results.append(cropped_img)

            # faceROI = frame_gray[y:y+h,x:x+w]
            # eyes = config.haarcascade_eyes_cascade.detectMultiScale(faceROI)
            # noses = config.haarcascade_nose_cascade.detectMultiScale(faceROI)
            # mouths = config.haarcascade_mouth_cascade.detectMultiScale(faceROI)
            # if (len(eyes) == 2):
            #     cropped_img = frame[y:y+h, x:x+w]
            #     results.append(cropped_img)

    return results

def extract_caffemodel_faces(frames):

    results = []

    for frame in frames:

        (h, w) = frame.shape[:2]
        blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))

        config.caffemodel_net.setInput(blob)
        detections = config.caffemodel_net.forward()

        for i in range(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence < config.caffemodel_confidence_threshold:
                continue

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            y = startY - 10 if startY - 10 > 10 else startY + 10
            
            cropped_img = frame[startY:endY, startX:endX]
            results.append(cropped_img)

    return results

def get_haarcascade_processed_frame(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    faces = config.haarcascade_face_cascade.detectMultiScale(
        frame_gray,
        scaleFactor=1.4,
        minNeighbors=1,
        minSize=(30,30)
    )
    for (x,y,w,h) in faces:
        faceROI = frame_gray[y:y+h,x:x+w]
        eyes = config.haarcascade_eyes_cascade.detectMultiScale(faceROI)
        noses = config.haarcascade_nose_cascade.detectMultiScale(faceROI)
        mouths = config.haarcascade_mouth_cascade.detectMultiScale(faceROI)
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
            cropped_img = frame[y:y+h, x:x+w]
            save_frame(cropped_img)
    return frame

def get_caffemodel_processed_frame(frame):

    (h, w) = frame.shape[:2]
    blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))

    config.caffemodel_net.setInput(blob)
    detections = config.caffemodel_net.forward()

    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence < config.caffemodel_confidence_threshold:
            continue

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        y = startY - 10 if startY - 10 > 10 else startY + 10
        
        cropped_img = frame[startY:endY, startX:endX]
        save_frame(cropped_img)

        if (config.draw_enabled):
            text = "{:.2f}%".format(confidence * 100)
            cv.rectangle(frame, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv.putText(frame, text, (startX, y),
            cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    return frame

def save_frame(frame):
    ts = str(time.time())
    path = os.path.join(config.DATA_DIR, str(int(config.PROGRAM_START_TIMESTAMP)), ts + ".png")
    cv.imwrite(path, frame)
    log.info("Saved " + path)
    return