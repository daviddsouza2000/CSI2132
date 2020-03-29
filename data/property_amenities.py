import pandas as pd

property_df = pd.read_csv("sample_properties.csv")

result_df = pd.DataFrame(columns=["AmenityName", "PropertyId"])

for i, prop in property_df.iterrows():
    items = prop["amenities"][1:-1].split(",")
    for item in items:
        # Remove quotes
        if item[0] == '"':
            item = item[1:-1]
        result_df = result_df.append(
            {"AmenityName": item, "PropertyId": prop["id"]}, ignore_index=True
        )


result_df.to_csv("sample_property_amenities.csv")
