from ultralytics import YOLO
import torch

def main():
    # 1. Initialize the model (YOLO26 Large)
    # The .pt file will automatically download on first run
    model = YOLO("yolo26l.pt")

    # 2. Check for CUDA (GTX 1080 Ti)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running inference on: {device}")

    # 3. Run Inference
    # source can be an image URL, local file, or folder
    results = model.predict(
        source="city-india.mp4",
        device=device,
        save=True,      # Save the output image to 'runs/detect/predict'
        conf=0.25       # Confidence threshold
    )

    # 4. Process Results
    for result in results:
        boxes = result.boxes
        print(f"Detected {len(boxes)} objects.")
        
        # Print detected classes and confidence
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            print(f" - Class: {model.names[cls]}, Confidence: {conf:.2f}")

if __name__ == "__main__":
    main()