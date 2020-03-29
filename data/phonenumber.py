import pandas as pd
import random as rand

user_df = pd.read_csv("sample_users.csv")
result_df = pd.DataFrame(columns=["PhoneNumber", "UserId"])

for i, row in user_df.iterrows():
    num = ""
    for x in range(10):
        num += str(rand.randint(1, 9))
    result_df = result_df.append(
        {"PhoneNumber": num, "UserId": row["UserId"]}, ignore_index=True
    )
result_df.to_csv("sample_phonenumbers.csv")
