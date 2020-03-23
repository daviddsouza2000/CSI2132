import pandas as pd
import random as rand

user_df = pd.read_csv("sample_users.csv")
property_df = pd.read_csv("sample_properties.csv")
user_ids = list(user_df["UserId"])

min_id = 1000
max_id = 999999
used_ids = set()
properties = property_df.sample(frac=0.9)

for i, prop in properties.iterrrows():
    booking_id = rand.randint(min_id, max_id)
    while(booking_id in used_ids):
        booking_id = rand.randint(min_id, max_id)
    used_ids.add(booking_id)
    user_id = rand.choice(user_ids)
    num_guests = rand.randint(1,int(prop["accommodates"]))



