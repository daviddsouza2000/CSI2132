import pandas as pd
import random as rand

property_df = pd.read_csv("sample_properties.csv")
branch_df = pd.read_csv("sample_branches.csv")

branch_ids = list(branch_df["BranchId"])

result_df = pd.DataFrame(columns = ["PropertyId", "HostId", "BranchId", "Title", "Description", "NumGuests", 
    "NumBedrooms", "NumBeds", "NumBaths"])

for i, prop in property_df.iterrows():
    property_id = prop["id"]
    host_id = prop["HostId"]
    branch_id = rand.choice(branch_ids)
    title = prop["name"]
    description = prop["description"]
    num_guests = prop["accommodates"]
    num_baths = prop["bathrooms"] 
    try:
        num_baths = int(num_baths)
    except:
        num_baths = 0

    num_bedrooms = prop["bedrooms"] 
    try:
        num_bedrooms = int(num_bedrooms)
    except:
        num_bedrooms = 0

    num_beds = prop["beds"] 
    try:
        num_beds = int(num_beds)
    except:
        num_beds = 0

    result_df = result_df.append({"PropertyId": property_id, "HostId": host_id, "BranchId": branch_id, "Title": title,
        "Description": description, "NumGuests": num_guests, "NumBedrooms": num_bedrooms, "NumBeds": num_beds,
        "NumBaths": num_beds}, ignore_index = True)

result_df.to_csv("sample_properties_clean.csv")

