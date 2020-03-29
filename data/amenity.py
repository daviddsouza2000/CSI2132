import pandas as pd

property_df = pd.read_csv("sample_properties.csv")
amenities = property_df["amenities"]

amenities_set = set()
for i in range(len(amenities)):
    items = amenities[i][1:-1].split(",")
    for item in items:
        # Remove quotes
        if item[0] == '"':
            item = item[1:-1]
        amenities_set.add(item)


result_df = pd.DataFrame(columns=["Name"])

for amenity in amenities_set:
    result_df = result_df.append({"Name": amenity}, ignore_index=True)

result_df.to_csv("sample_amenities.csv")
