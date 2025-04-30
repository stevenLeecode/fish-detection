from roboflow import Roboflow

rf = Roboflow(api_key="hrFssYd8V4XFC2kFVjfU")
project = rf.workspace("fishdetection-jktko").project("fish-detection-8jhpr")
version = project.version(2)
dataset = version.download("yolov8")