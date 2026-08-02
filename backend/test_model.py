from app.ml.model_loader import model_loader

model = model_loader.load()

print(type(model))

print("Model Loaded Successfully")