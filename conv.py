from ultralytics import YOLO

# Load a model
model = YOLO("runs/detect/train/weights/best.pt")

# Export the model
model.export(format='tflite')
