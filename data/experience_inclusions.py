import pandas as pd
import random as rand

inclusion_df = pd.read_csv("sample_inclusions.csv")
experience_df = pd.read_csv("sample_experiences.csv")

inclusions = list(inclusion_df["Name"])
experience_ids = list(experience_df["ExperienceId"])

min_inclusions = 1
max_inclusions = 10

result_df = pd.DataFrame(columns = ["InclusionName", "ExperienceId"])

for _id in experience_ids:
    num_inclusions = rand.randint(min_inclusions, max_inclusions)
    used_inclusions = set()
    for i in range(num_inclusions):
        inclusion = rand.choice(inclusions)
        while(inclusion in used_inclusions):
            inclusion = rand.choice(inclusions)
        used_inclusions.add(inclusion)
        result_df = result_df.append({"InclusionName":inclusion, "ExperienceId": _id }, ignore_index = True)

result_df.to_csv("sample_experience_inclusions.csv")
        

