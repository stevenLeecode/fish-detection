from picamera2 import Picamera2, Preview
from datetime import datetime
import time
import subprocess
from picamera2.encoders import H264Encoder

time.sleep(30)
#Setup
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size":(1920, 1080)})
picam2.set_controls({"ScalerCrop" : (0, 0, 2592, 1700)})
picam2.configure(config)

time.sleep(2)

picam2.start()
encoder_bitrate = 10000000
h264_filename = "output_video.h264"
mp4_filename = "output_video2.mp4"
encoder = H264Encoder(bitrate=10000000)
print("Sleeping to give time to start recording")
time.sleep(3)
picam2.start_recording(encoder, h264_filename)

record_time = 40
print(f"Sleeping for {record_time} secs, currently recording.")
time.sleep(record_time)
picam2.stop_recording()

subprocess.run([
    "ffmpeg", "-y", "-framerate", "30", "-i", h264_filename,
    "-c", "copy", mp4_filename
    ])

print("Video saved as: ", mp4_filename)
