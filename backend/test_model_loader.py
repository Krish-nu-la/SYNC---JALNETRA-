from app.ml.model_loader import model_loader

model_loader.load()

print(type(model_loader.model))

print(model_loader.encoders.keys())

print(model_loader.features)