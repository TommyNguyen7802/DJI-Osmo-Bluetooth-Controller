#Eun yolo for vedio output
import cv2
from ultralytics import YOLO


def main():
    print("Starting YOLO webcam detection...")

    # name of the model
    model = YOLO("example.pt")

    cap = cv2.VideoCapture(0)

    # Check if camera opened
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

        # Run YOLO detection
        results = model(frame)

        boxes = results[0].boxes

        # Count valid detections (with confidence filter)
        num_objects = 0
        score = 0

        if boxes is not None:
            for box in boxes:
                conf = float(box.conf[0])

                # Ignore weak detections
                if conf < 0.5:
                    continue

                num_objects += 1

                # Get class label
                cls = int(box.cls[0])
                label = model.names[cls]

                # Weight different trash types (customize this)
                if label in ["bottle", "can"]:
                    score += 1
                elif label in ["trash", "garbage", "bag"]:
                    score += 2
                else:
                    score += 1  # default weight

        # Cleanliness logic (based on score, not just count)
        if score <= 2:
            status = "Clean"
            color = (0, 255, 0)
        elif score <= 6:
            status = "Messy"
            color = (0, 255, 255)
        else:
            status = "Dirty"
            color = (0, 0, 255)

        annotated_frame = results[0].plot()

        # Display info
        text1 = f"Objects: {num_objects}"
        text2 = f"Score: {score} | Status: {status}"

        cv2.putText(annotated_frame, text1, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.putText(annotated_frame, text2, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Show frame
        cv2.imshow("YOLO Cleanliness Detection", annotated_frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Webcam detection stopped.")


if __name__ == "__main__":
    main()
    
    
    
