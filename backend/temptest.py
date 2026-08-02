import joblib

encoders = joblib.load("app/ml/models/encoders.pkl")

print("Land Cover:", encoders["land_cover"].classes_)
print("Soil Type:", encoders["soil_type"].classes_)