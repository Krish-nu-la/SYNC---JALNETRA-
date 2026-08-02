import joblib

features = joblib.load("app/ml/models/feature_columns.pkl")

print(features)