import cv2
from ultralytics import YOLO

# Load the model
model = YOLO("yolov8n.pt")

# Load the video
cap = cv2.VideoCapture("output_video.mp4")

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    results = model.predict(source=frame, conf=0.25, device='cpu')

    annotated_frame = results[0].plot()
    
    cv2.imshow("YOLOv8 Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()