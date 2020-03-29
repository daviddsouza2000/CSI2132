import pandas as pd
import random as rand

payment_df = pd.read_csv("sample_payments.csv")
booking_df = pd.read_csv("sample_property_bookings.csv")

booking_df.drop(booking_df.filter(regex="Unname"), axis=1, inplace=True)

result_df = pd.DataFrame(columns=["PaymentId", "PropertyId", "BookingId"])

bookings = list(booking_df.values)

for i, payment in payment_df.iterrows():
    booking = rand.choice(bookings)
    result_df = result_df.append(
        {
            "PaymentId": payment["PaymentId"],
            "PropertyId": int(booking[1]),
            "BookingId": int(booking[0]),
        },
        ignore_index=True,
    )

result_df.to_csv("sample_property_payments.csv")
