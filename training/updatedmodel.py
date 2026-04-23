import cv2
from ultralytics import YOLO
import os


def main():
    print("Running YOLO on image...")

    # Load model
    model = YOLO("model7.pt")

    # Load image
    image_path = "picture5.jpg"
    frame = cv2.imread(image_path)

    if frame is None:
        print("❌ Error: Could not load image.")
        return

    # Run YOLO detection
    results = model(frame)
    boxes = results[0].boxes

    num_objects = 0
    score = 0
    object_counts = {}

    if boxes is not None:
        for box in boxes:
            conf = float(box.conf[0])

            if conf < 0.5:
                continue

            num_objects += 1

            cls = int(box.cls[0])
            label = model.names[cls]

            # Count objects
            object_counts[label] = object_counts.get(label, 0) + 1

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

    # Cleanliness percentage
    max_possible = num_objects * 2 if num_objects > 0 else 1
    cleanliness_percent = max(0, 100 - int((score / max_possible) * 100))

    # Text summaries
    summary = f"Detected {num_objects} objects"
    details = f"Score: {score} | Status: {status}"
    percent_text = f"Cleanliness: {cleanliness_percent}%"
    breakdown = ", ".join([f"{k}:{v}" for k, v in object_counts.items()])

    # Annotate frame
    annotated_frame = results[0].plot()

    if annotated_frame is None:
        print("❌ Error: Annotated frame is empty.")
        return

    # Background banner
    cv2.rectangle(annotated_frame, (10, 10), (600, 150), (0, 0, 0), -1)

    # Overlay text
    cv2.putText(annotated_frame, summary, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.putText(annotated_frame, details, (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.putText(annotated_frame, percent_text, (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.putText(annotated_frame, f"Types: {breakdown}", (20, 145),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show image
    cv2.imshow("YOLO Cleanliness Detection", annotated_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ✅ SAFE IMAGE SAVE (FIXED)
    print("Current working directory:", os.getcwd())

    output_path = os.path.join(os.getcwd(), "output.jpg")

    success = cv2.imwrite(output_path, annotated_frame)

    if success:
        print(f"✅ Image saved successfully at: {output_path}")
    else:
        print("❌ Failed to save image")

    # Console report
    print("\n--- CLEANLINESS REPORT ---")
    print(f"Objects detected: {num_objects}")
    print(f"Score: {score}")
    print(f"Status: {status}")
    print(f"Cleanliness: {cleanliness_percent}%")
    print(f"Breakdown: {object_counts}")

    # Save report
    with open("report.txt", "w") as f:
        f.write("CLEANLINESS REPORT\n")
        f.write(f"Objects: {num_objects}\n")
        f.write(f"Score: {score}\n")
        f.write(f"Status: {status}\n")
        f.write(f"Cleanliness: {cleanliness_percent}%\n")
        f.write(f"Breakdown: {object_counts}\n")

    print("📄 Report saved as report.txt")


if __name__ == "__main__":
    main()