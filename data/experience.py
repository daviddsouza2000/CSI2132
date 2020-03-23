import pandas as pd
import random as rand

user_df = pd.read_csv("sample_users.csv")
branch_df = pd.read_csv("sample_branches.csv")
branch_ids = list(branch_df["BranchId"])
user_ids = list(user_df["UserId"])
min_id = 1000
max_id = 999999
used_ids = set()
num_experiences = 200

result_df = pd.DataFrame(columns = ["ExperienceId", "HostId", "BranchId", "Title", "Description", "Duration", "GroupSize"])

for i in range(num_experiences):
    exp_id = rand.randint(min_id, max_id)
    while(exp_id in used_ids):
        exp_id = rand.randint(min_id, max_id)
    used_ids.add(exp_id)
    host_id = rand.choice(user_ids)
    branch_id = rand.choice(branch_ids)
    title = "Title" + str(i+1)
    description = "Description" + str(i + 1)
    group_size = rand.randint(1, 8)

    duration_template = "{0}:{1}:00"
    hours = rand.randint(0, 12)
    minutes = rand.randint(0, 59)
    if(hours < 10):
        hours = "0" + str(hours)
    if(minutes < 10):
        minutes = "0" + str(minutes)
    duration = duration_template.format(hours, minutes)

    result_df = result_df.append({"ExperienceId": exp_id, "HostId": host_id, "BranchId": branch_id, "Title": title,
        "Description": description, "Duration": duration, "GroupSize": group_size}, ignore_index=True)
result_df.to_csv("sample_experiences.csv")
