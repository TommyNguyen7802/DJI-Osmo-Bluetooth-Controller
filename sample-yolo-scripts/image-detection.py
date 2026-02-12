from ultralytics import YOLO

def main():
    print("Hello, World!")

    model = YOLO("yolo26n.pt")

    results = model.predict(source="https://ultralytics.com/images/bus.jpg", save=True)

    print(f"Success! Result saved to: {results[0].save_dir}")

if __name__ == "__main__":
    main()