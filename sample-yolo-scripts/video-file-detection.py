from ultralytics import YOLO

def main():
    print("Hello, World!")

    model = YOLO("yolo26n.pt")

    model.export(format="openvino")
    optimized_model = YOLO("yolo26n_openvino_model/")

    results = optimized_model.predict(source="city-india.mp4", show=True, save=True)

    print(f"Success! Result saved to: {results[0].save_dir}")

if __name__ == "__main__":
    main()