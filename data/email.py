import pandas as pd
import random as rand

user_df = pd.read_csv("sample_users.csv")
result_df = pd.DataFrame(columns = ["Email", "UserId"])

for i, row in user_df.iterrows():
    template = "{0}.{1}{2}@mail.com"
    email = template.format(row["FirstName"], row["LastName"], i)
    result_df = result_df.append({"Email": email, "UserId": row["UserId"]}, ignore_index=True)
result_df.to_csv("sample_email.csv")
