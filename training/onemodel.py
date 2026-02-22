# This file is for testing one model at a time
import cv2
from ultralytics import YOLO


def main():
    print("Starting YOLO webcam detection...")

    # Load YOLO model (downloaded automatically first time)
    model = YOLO("waste.pt")

    cap = cv2.VideoCapture(0)

    # Check if camera opened
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    # capture frame per second
    camera_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second: {camera_fps}")
     
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        results = model(frame)

        annotated_frame = results[0].plot()

        # Show the frame
        cv2.imshow("YOLO Webcam Detection", annotated_frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam detection stopped.")


if __name__ == "__main__":
    main()

