import cv2
from ultralytics import YOLO


def main():
    print("Starting YOLO video detection...")

    # Load YOLO model
    model = YOLO("Model name")

    # Input video file
    video = "path to vedio"

    # Open video
    cap = cv2.VideoCapture(video)

    # Check if video opened
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Frames per second: {fps}")

    # Output video file
    output_video = "output_video.mp4"

    # Video writer (saves processed video)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()

        # Stop when video ends
        if not ret:
            print("Video finished.")
            break

        # Run YOLO detection
        results = model(frame)

        boxes = results[0].boxes

        # Count valid detections
        num_objects = 0.0
        mess_score = 0.0

        if boxes is not None:
            for box in boxes:
                conf = float(box.conf[0])

                # Ignore weak detections
                if conf < 0.25:
                    continue

                num_objects += 1

                # Get class label
                cls = int(box.cls[0])
                label = model.names[cls]

                # Score logic
                if label == "messy":
                    mess_score += conf * 20
                else:
                    mess_score += conf * 10

        # Cleanliness calculation
        cleanliness = max(0, 100 - int(mess_score))

        if cleanliness >= 80:
            status = "Clean"
            color = (0, 255, 0)  # Green
        elif cleanliness >= 50:
            status = "Messy"
            color = (0, 255, 255)  # Yellow
        else:
            status = "Dirty"
            color = (0, 0, 255)  # Red

        # Draw YOLO detections
        annotated_frame = results[0].plot()

        # Dark transparent background box
        overlay = annotated_frame.copy()
        cv2.rectangle(overlay, (20, 20), (900, 320), (0, 0, 0), -1) 
        alpha = 0.6
        
        annotated_frame = cv2.addWeighted( overlay, alpha, annotated_frame, 1 - alpha, 0)

        # Display text
        cv2.putText( annotated_frame, "CLEANLINESS REPORT", (40, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3 )

        cv2.putText( annotated_frame, f"Number of surfaces: {int(num_objects)}", (40, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2 )

        cv2.putText( annotated_frame, f"Cleanliness: {cleanliness}", (40, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2 )

        cv2.putText( annotated_frame,f"Status: {status}",(40, 260),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Console output
        print("\n===== CLEANLINESS REPORT =====")
        print(f"Number of surfaces: {num_objects}")
        print(f"Cleanliness: {cleanliness}")
        print(f"Status: {status}")

        # Show live frame
        cv2.imshow("YOLO Video Detection", annotated_frame)

        # Save frame to output video
        out.write(annotated_frame)

        # Press q to stop early
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Processed video saved as: {output_video}")


if __name__ == "__main__":
    main()
