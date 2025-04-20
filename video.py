from picamera2 import Picamera2, Preview
from datetime import datetime
import time
import subprocess
from picamera2.encoders import H264Encoder

#Setup
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size":(1920, 1080)})
picam2.configure(config)

time.sleep(2)

sens_width, sens_height = picam2.camera_properties["PixelArraySize"]
crop_x = 100
crop_y = sens_height // 4
crop_w = sens_width - 100
crop_h = (sens_height * 3) // 4

picam2.set_controls({"ScalerCrop" : (crop_x, crop_y+200, crop_w, crop_h-350)})
print("crop settings: ", crop_x, crop_y, crop_w, crop_h)
print("scaler crop: ", picam2.camera_controls['ScalerCrop'])
time.sleep(1)

picam2.start()
encoder_bitrate = 10000000
h264_filename = "output_video.h264"
mp4_filename = "output_video.mp4"
encoder = H264Encoder(bitrate=10000000)
print("Sleeping to give time to start recording")
time.sleep(3)
picam2.start_recording(encoder, h264_filename)

record_time = 200
print(f"Sleeping for {record_time} secs, currently recording.")
time.sleep(record_time)
picam2.stop_recording()

subprocess.run([
    "ffmpeg", "-y", "-framerate", "30", "-i", h264_filename,
    "-c", "copy", mp4_filename
    ])

print("Video saved as: ", mp4_filename)
