from app.ml.predictor import predictor

results = predictor.predict(
    rainfall=70,
    offset=60
)

for r in results:
    print(
        r["zone"]["name"],
        "->",
        r["depth_cm"],
        "cm"
    )