import cv2
from ultralytics import YOLO


def main():
    print("Starting YOLO dual-model webcam detection...")

    # Load BOTH models
    coco_model = YOLO("yolo26n.pt")   # Pretrained COCO
    waste_model = YOLO("waste.pt")     # Your trained model

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    camera_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second: {camera_fps}")
     
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Run inference on BOTH models
        coco_results = coco_model(frame)
        waste_results = waste_model(frame)

        # Draw results
        annotated_frame = frame.copy()

        # Plot COCO detections
        annotated_frame = coco_results[0].plot(img=annotated_frame)

        # Plot Waste detections ON TOP
        annotated_frame = waste_results[0].plot(img=annotated_frame)

        cv2.imshow("YOLO Dual Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Webcam detection stopped.")


if __name__ == "__main__":
    main()
