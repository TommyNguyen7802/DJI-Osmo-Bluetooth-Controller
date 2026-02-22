from ultralytics import YOLO

def main():
    print("Starting training...")

    model = YOLO("yolo26n.pt")

    model.train(
        # data="/Users/osvat0rres/Desktop/archive/YOLO-Waste-Detection-1/YOLO-Waste-Detection-1/data.yaml",
        data = "C:/datasets/archive/YOLO-Waste-Detection-1/YOLO-Waste-Detection-1/data.yaml",
        epochs=50,
        imgsz=640,
        batch=8
    )

if __name__ == "__main__":
    main()
    
