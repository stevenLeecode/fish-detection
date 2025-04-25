from picamera2 import Picamera2, Preview
from datetime import datetime
import time

#Setup
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size":(2592, 1944)})
picam2.configure(config)

time.sleep(2)

sens_width, sens_height = picam2.camera_properties["PixelArraySize"]
crop_x = 100
crop_y = sens_height // 4
crop_w = sens_width - 100
crop_h = (sens_height * 3) // 4

#picam2.set_controls({"ScalerCrop" : (crop_x, crop_y+200, crop_w, crop_h-350)})
#print("crop settings: ", crop_x, crop_y, crop_w, crop_h)
#print("scaler crop: ", picam2.camera_controls['ScalerCrop'])
time.sleep(1)

#main loop
picam2.start()
pic_counter = 1
while True:
    filename = f'images/picture{pic_counter}.jpg'
    picam2.capture_file(filename)
    time.sleep(1.5)
    pic_counter += 1
picam2.stop()
