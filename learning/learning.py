import os
from ultralytics import YOLO


model = YOLO("./yolo/runs/detect/train/best.py") 
model.train(data="dataset.yaml", epochs=100, batch=16, workers=4, degrees=90.0)
