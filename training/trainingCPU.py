from ultralytics import YOLO

def main():
    print("Starting training...")

    model = YOLO("yolo26n.pt")

    model.train(
       
        #place the path to the .yaml file here
        data = " ",
        epochs=50,
        imgsz=640,
        batch=8
    )

if __name__ == "__main__":
    main()
    
