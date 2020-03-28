import pandas as pd
import random as rand

language_df = pd.read_csv("sample_languages.csv")
experience_df = pd.read_csv("sample_experiences.csv")

languages = list(language_df["Name"])
experience_ids = list(experience_df["ExperienceId"])

min_languages = 1
max_languages = 10

result_df = pd.DataFrame(columns = ["LanguageName", "ExperienceId"])

for _id in experience_ids:
    num_languages = rand.randint(min_languages, max_languages)
    used_languages = set()
    for i in range(num_languages):
        language = rand.choice(languages)
        while(language in used_languages):
            language = rand.choice(languages)
        used_languages.add(language)
        result_df = result_df.append({"LanguageName":language, "ExperienceId": _id }, ignore_index = True)

result_df.to_csv("sample_experience_languages.csv")
        

