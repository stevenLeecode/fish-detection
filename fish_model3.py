from ultralytics import YOLO
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np


model = YOLO("runs\\detect\\train\\weights\\best.pt", verbose=False)

tracker = DeepSort(
    max_age=3,
    n_init=3,
    max_iou_distance=0.7,
)


#video_path = "resized_output_video.mp4"
video_path = "output_video2.mp4"

cap = cv2.VideoCapture(video_path)
original_fps = cap.get(cv2.CAP_PROP_FPS)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("End of video or error reading the video.")
        break


    # Run prediction on single frame
    results = model(frame, conf=0.25, verbose=False)

    detections = []
    for result in results[0].boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = result
        #print(f"Detection: {x1}, {y1}, {x2}, {y2}, {conf}, {cls}")
        bbox = np.array([x1, y1, x2-x1, y2-y1]) # x, y, width, height of bbox
        detections.append((bbox, conf, 'fish'))

    tracks = tracker.update_tracks(detections, frame=frame)
    

    #Print number of fish detected
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        bbox = track.to_tlwh()
        x1, y1, w, h = bbox
        x2, y2 = int(x1 + w), int(y1 + h)
        confidence = track.get_det_conf()
        
        #print(f"Track ID: {track_id}, BBox: {bbox}, Confidence: {confidence}")
        
        # Draw bounding box and track ID on the frame
        #cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        #cv2.putText(frame, f"ID: {track_id}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if confidence is not None:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track_id}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Conf: {confidence:.2f}", (int(x1), int(y1) - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Track history for visualization

    
    # Visualize results on the frame
    # Display the annotated frame
    cv2.imshow("YOLO11 Tracking", frame)
    #out.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release
cv2.destroyAllWindows()