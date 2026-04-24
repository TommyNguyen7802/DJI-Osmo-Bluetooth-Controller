import cv2
from ultralytics import YOLO


def main():
    print("Running YOLO on image...")

    # Load model
    model = YOLO("name of the model")

    # Load image
    image_path = "image"
    frame = cv2.imread(image_path)

    if frame is None:
        print("Error: Could not load image.")
        return

    # Run YOLO detection
    results = model(frame)
    boxes = results[0].boxes

    num_objects = 0
    mess_score = 0.0

    # -------- DETECTION + SCORING --------
    if boxes is not None:
        for box in boxes:
            conf = float(box.conf[0])

            # Lower threshold so your detections count
            if conf < 0.25:
                continue

            num_objects += 1

            cls = int(box.cls[0])
            label = model.names[cls]

            # Cleanliness scoring (based on your "messy" model)
            if label == "messy":
                mess_score += conf * 20   # adjust weight if needed
            else:
                mess_score += conf * 10

    # Convert to cleanliness %
    cleanliness = max(0, 100 - int(mess_score))

    # -------- STATUS LOGIC --------
    if cleanliness >= 80:
        status = "Clean"
        color = (0, 255, 0)
    elif cleanliness >= 50:
        status = "Messy"
        color = (0, 255, 255)
    else:
        status = "Dirty"
        color = (0, 0, 255)

    # -------- DRAW YOLO RESULTS --------
    annotated_frame = results[0].plot()

    # -------- MENU OVERLAY (BOX UI) --------
    # 
    overlay = annotated_frame.copy()
    cv2.rectangle(overlay, (10, 10), (790, 350), (0, 0, 0), -1)
    alpha = 0.6
    annotated_frame = cv2.addWeighted(overlay, alpha, annotated_frame, 1 - alpha, 0)

    # Text settings
    cv2.putText(annotated_frame, "CLEANLINESS REPORT", (50, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

    cv2.putText(annotated_frame, f"Number of Surfaces: {num_objects}", (40, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)

    cv2.putText(annotated_frame, f"Cleanliness: {cleanliness}%", (40, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)

    cv2.putText(annotated_frame, f"Status: {status}", (40, 270),
                cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)
    
    # -------- CONSOLE OUTPUT --------
    print("\n===== CLEANLINESS REPORT =====")
    print(f"Number of Surfaces: {num_objects}")
    print(f"Cleanliness      : {cleanliness}%")
    print(f"Status           : {status}")
    print("==============================\n")

    # # -------- USER MENU --------
    # print("Choose an option:")
    # print("1. Show Image")
    # print("2. Save Image")
    # print("3. Show & Save")
    # print("4. Exit")

    # choice = input("Enter choice: ")

    # if choice == "1":
    #     cv2.imshow("YOLO Image Detection", annotated_frame)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # elif choice == "2":
    #     cv2.imwrite("output.jpg", annotated_frame)
    #     print("Saved as output.jpg")

    # elif choice == "3":
    cv2.imshow("YOLO Image Detection", annotated_frame)
    cv2.imwrite("output.jpg", annotated_frame)
    print("Saved as output.jpg")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # else:
    #     print("Exiting...")

    # print("Done.")


if __name__ == "__main__":
    main()
