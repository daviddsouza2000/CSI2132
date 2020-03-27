import pandas as pd
import random as rand
from datetime import timedelta, datetime

#https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = rand.randrange(int_delta)
    return start + timedelta(seconds=random_second)

user_df = pd.read_csv("sample_users.csv")
experience_df = pd.read_csv("sample_experiences.csv")
user_ids = list(user_df["UserId"])

min_id = 1000
max_id = 999999
used_ids = set()
min_price = 200
max_price = 1000
experiences = experience_df.sample(frac=0.9)
min_date = datetime.strptime('1/1/2008 01:30', '%m/%d/%Y %I:%M')
max_date  = datetime.strptime('1/1/2020 4:50', '%m/%d/%Y %I:%M')

result_df = pd.DataFrame(columns = ["BookingId", "ExperienceId", "UserId", "NumGuests", "DateBooked", "StartDateTime", "EndDateTime", "Price"])

for i, exp in experiences.iterrows():
    booking_id = rand.randint(min_id, max_id)
    while(booking_id in used_ids):
        booking_id = rand.randint(min_id, max_id)
    used_ids.add(booking_id)
    user_id = rand.choice(user_ids)
    num_guests = rand.randint(1,int(exp["GroupSize"]))
    booking_date = random_date(min_date, max_date)
    start_date = random_date(booking_date, max_date)
    
    dur_decomposition = exp["Duration"].split(":")
    hours = int(dur_decomposition[0])
    minutes = int(dur_decomposition[1])
    seconds = int(dur_decomposition[2])

    end_date = start_date + timedelta(hours=hours, minutes=minutes, seconds=seconds)

    price = rand.randint(min_price, max_price)

    result_df = result_df.append({"BookingId": booking_id, "ExperienceId": exp["ExperienceId"], "UserId": user_id, 
        "NumGuests": num_guests, "DateBooked": booking_date, "StartDateTime": start_date, "EndDateTime": end_date,
        "Price": price }, ignore_index = True)

result_df.to_csv("sample_experience_bookings.csv")
        

