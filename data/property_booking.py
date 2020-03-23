import pandas as pd
import random as rand

user_df = pd.read_csv("sample_users.csv")
property_df = pd.read_csv("sample_properties.csv")
user_ids = list(user_df["UserId"])

min_id = 1000
max_id = 999999
used_ids = set()
properties = property_df.sample(frac=0.95)

for prop in properties:


