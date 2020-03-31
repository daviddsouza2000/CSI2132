import pandas as pd
import random as rand

experience_df = pd.read_csv("sample_experiences.csv")

result_df = pd.DataFrame(
    columns=[
        "ExperienceId",
        "HostId",
        "BranchId",
        "Title",
        "Description",
        "Duration",
        "GroupSize",
        "Price",
    ]
)

for _, exp in experience_df.iterrows():
    result_df = result_df.append(
        {
            "ExperienceId": exp["ExperienceId"],
            "HostId": exp["HostId"],
            "BranchId": exp["BranchId"],
            "Title": exp["Title"],
            "Description": exp["Description"],
            "Duration": exp["Duration"],
            "GroupSize": exp["GroupSize"],
            "Price": rand.randint(100, 2000),
        },
        ignore_index=True,
    )

result_df.to_csv("sample_experiences.csv")
