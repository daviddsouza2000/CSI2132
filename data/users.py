import pandas as pd
import random as rand

names_df = pd.read_csv("temp/names.csv")
address_df = pd.read_csv("temp/addresses.csv", low_memory=False)

# set is used first to remove duplicates
first_names = list(set(names_df["FirstName"]))
last_names = list(set(names_df["Surname"]))
streets = list(set(address_df["STREET"]))
cities = list(set(address_df["CITY"]))
cities = cities[1:] #first element is nan
provinces = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
super_host_chance = 0.05
min_id = 1000
max_id = 999999
min_house_number = 1
max_house_number = 5000
num_users = 500
used_ids = set()
result_df = pd.DataFrame(columns = ["UserId", "FirstName", "LastName", "HouseNumber", "Street", "City", "Province", "IsSuperHost"])

for i in range(num_users):
    user_id = rand.randint(min_id, max_id) 
    while(user_id in used_ids):
        user_id = rand.randint(min_id, max_id) 
    used_ids.add(user_id)

    first_name = rand.choice(first_names)
    last_name = rand.choice(last_names)
    house_number = rand.randint(min_house_number, max_house_number)
    street = rand.choice(streets)
    city = rand.choice(cities)
    province = rand.choice(provinces)
    is_super_host = rand.uniform(0, 1) > 1 - super_host_chance

    result_df = result_df.append({"UserId": user_id, "FirstName": first_name, 
        "LastName": last_name, "HouseNumber": house_number, "Street": street, "City": city, 
        "Province": province, "IsSuperHost": is_super_host}, ignore_index = True)

result_df.to_csv("sample_users.csv")


