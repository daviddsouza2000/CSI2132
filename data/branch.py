import pandas as pd
import random as rand

user_df = pd.read_csv("sample_users.csv")
user_ids = user_df["UserId"]
result_df = pd.DataFrame(columns = ["BranchId", "ManagerId", "Name"])

min_id = 1000
max_id = 999999
num_branches = 3
used_ids = set()

for i in range(num_branches):
    branch_id = rand.randint(min_id, max_id)
    while(branch_id in used_ids):
        branch_id = rand.randint(min_id, max_id)
    used_ids.add(branch_id)
    manager_id = rand.choice(user_ids)
    name = "branch" + str(i + 1)
    result_df = result_df.append({"BranchId": branch_id, "ManagerId": manager_id, "Name": name}, ignore_index=True)

result_df.to_csv("sample_branches.csv")

