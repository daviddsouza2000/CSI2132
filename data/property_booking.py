import pandas as pd
import random as rand

user_df = pd.read_csv("sample_users.csv")
property_df = pd.read_csv("sample_properties.csv")

min_id = 1000
max_id = 999999
used_ids = set()
