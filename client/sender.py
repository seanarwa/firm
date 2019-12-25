import os
import requests
import logging as log
import json

# local modules
import config

HTTP_HEADERS = {'Content-type': 'application/json'}

def connect():

    if not config.data_service_enabled:
        log.error("Unable to connect data sender: data service option is disabled")
        return False

    log.info("Attempting to connect to firm-fms ...")
    log.info("/GET %s", config.data_service_host)
    response = requests.get(config.data_service_host)

    log.info("firm-fms response body: %s", response.content)

    if response.status_code != 200:
        log.error("Error occured when trying to connect to %s", config.data_service_host)
        log.error("Status code: %d", response.status_code)
        return False
    
    log.info("Successfully connected to firm-fms")
    return True

def send_image(image_file_name):

    log.debug("Sending image %s to firm-fms ...", image_file_name)

    image_file_path = os.path.join(config.image_output_directory, image_file_name)
    with open(image_file_path, 'rb') as img_file:
        files = {'image': img_file}
        data = {'name': image_file_name}
        response = requests.post(config.data_service_host, files=files, data=data)
        if response.status_code == 200:
            log.debug("Image successfully sent to firm-fms")
        else:
            log.error("Error occured when trying to send image to firm-fms")

    return

def send_frame(frame):

    log.debug("Sending frame to firm-fms ...")

    data = {'image': 'hello'}
    response = requests.post(config.data_service_host, data=json.dumps(data), headers=HTTP_HEADERS)
    if response.status_code == 200:
        log.debug("Frame successfully sent to firm-fms")
    else:
        log.error("Error occured when trying to send frame to firm-fms, status code: %s", response.status_code)
    # threading.Thread(target=send_request, args=(config.data_service_host, data, HTTP_HEADERS)).start()

    return

def send_request(host, data, headers):

    response = requests.post(host, data=data, headers=headers)
    if response.status_code == 200:
        log.debug("Frame successfully sent to firm-fms")
    else:
        log.error("Error occured when trying to send frame to firm-fms, status code: %s", response.status_code)

    return