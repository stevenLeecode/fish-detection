from ultralytics import YOLO
# Load model architecture (you can start with yolov8n for lightweight, or yolov8s/yolov8m/yolov8l/yolov8x)
model = YOLO("yolov8n.pt")  # or "yolov8n.pt" to start from pretrained weights
# Train the model
model.train(data="Fish-detection-2/data.yaml", epochs=20, imgsz=640)

results = model.predict(source="images\\picture32.jpg", save=True)