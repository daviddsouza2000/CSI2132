import pandas as pd

num_languages = 50

result_df = pd.DataFrame(columns=["Name"])

for i in range(1, num_languages + 1):
    result_df = result_df.append({"Name": "Language{0}".format(i)}, ignore_index=True)
result_df.to_csv("sample_languages.csv")
