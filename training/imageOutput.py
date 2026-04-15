# Run model with imaga
import cv2
from ultralytics import YOLO


def main():
    print("Running YOLO on image...")

    # Load model
    model = YOLO("12class.pt")

    # Load image
    image_path = "after.png"   
    frame = cv2.imread(image_path)

    if frame is None:
        print("Error: Could not load image.")
        return

    # Run YOLO detection
    results = model(frame)
    boxes = results[0].boxes

    num_objects = 0
    score = 0

    if boxes is not None:
        for box in boxes:
            conf = float(box.conf[0])

            if conf < 0.5:
                continue

            num_objects += 1

            cls = int(box.cls[0])
            label = model.names[cls]

            # Scoring logic
            if label in ["bottle", "can"]:
                score += 1
            elif label in ["trash", "garbage", "bag"]:
                score += 2
            else:
                score += 1

    # Cleanliness logic
    if score <= 2:
        status = "Clean"
        color = (0, 255, 0)
    elif score <= 6:
        status = "Messy"
        color = (0, 255, 255)
    else:
        status = "Dirty"
        color = (0, 0, 255)

    # Draw results
    annotated_frame = results[0].plot()

    text1 = f"Objects: {num_objects}"
    text2 = f"Score: {score} | Status: {status}"

    cv2.putText(annotated_frame, text1, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.putText(annotated_frame, text2, (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Show image
    cv2.imshow("YOLO Image Detection", annotated_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Optional: save result
    cv2.imwrite("output.jpg", annotated_frame)
    print("Done. Saved as output.jpg")


if __name__ == "__main__":
    main()
