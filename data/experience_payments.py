import pandas as pd
import random as rand

payment_df = pd.read_csv("sample_payments.csv")
booking_df = pd.read_csv("sample_experience_bookings.csv")

result_df = pd.DataFrame(columns=["PaymentId", "ExperienceId", "BookingId"])

bookings = list(booking_df.values)

for i, payment in payment_df.iterrows():
    booking = rand.choice(bookings)
    result_df = result_df.append({"PaymentId": payment["PaymentId"], "ExperienceId": booking[1], "BookingId": booking[0]}, ignore_index = True)

result_df.to_csv("sample_experience_payments.csv")

