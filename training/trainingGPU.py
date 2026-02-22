
# trining file with GPU
from ultralytics import YOLO


def main():
    
    print("Stating training")

    model = YOLO("yolov8n.pt")  # or yolov8s.pt / yolov8m.pt

    # start trining 
    model.train(
        
        #path to .yaml file   
        data="",
        # amount of time the model will see the images
        epochs=50,
        #size of the image been trine
        imgsz=640,
        #
        batch=4,
        # Use GPU if available (device=0 for first GPU)
        device=0,
        
        save=True,
        half=True,
    )


if __name__ == "__main__":
    main()
 