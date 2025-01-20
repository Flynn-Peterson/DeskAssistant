from ultralytics import YOLO

# Load a pre-trained YOLOv8 model (e.g., yolov8n.pt for YOLOv8 nano version)
model = YOLO("yolov8n.pt")

# Train the model on your dataset
results = model.train(data='C:/PersonalProjects/RoboArm/commonDesk/data.yaml', epochs=300, imgsz=640, batch=16)
