import pandas as pd
import random

user_df = pd.read_csv("sample_users.csv")
experience_df = pd.read_csv("sample_experiences.csv")

min_id = 1000
max_id = 999999
used_ids = set()
num_reviews = 1000
experience_ids  = experience_df["ExperienceId"]
user_ids = user_df["UserId"]

result_df = pd.DataFrame(columns = ["ReviewId", "ExperienceId", "UserId", "Description", "Rating", "Communications", "Value"]) 

for i in range(num_reviews):
    review_id = random.randint(min_id, max_id)
    while(review_id in used_ids):
        review_id = random.randint(min_id, max_id)

    used_ids.add(review_id)
    exp_id  = random.choice(experience_ids)
    user_id = random.choice(user_ids)
    description = "Review{0}".format(i+1)
    rating = random.randint(1, 5)
    communications = random.randint(1, 5)
    value = random.randint(1, 5)
    result_df = result_df.append({"ReviewId": review_id, "ExperienceId": exp_id, "UserId": user_id, "Description": description, "Rating": rating, "Communications": communications,  "Value": value},
            ignore_index = True)
result_df.to_csv("sample_exp_reviews.csv")

