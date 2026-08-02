from app.ml.feature_builder import feature_builder

df = feature_builder.build(

    rainfall=70,

    offset=60

)

print(df.head())

print()

print(df.columns.tolist())