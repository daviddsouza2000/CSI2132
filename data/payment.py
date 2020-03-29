import pandas as pd
import random as rand

types = ["cash", "debit", "credit"]
statuses = ["completed", "approved", "pending"]

num_payments = 2000
min_id = 1000
max_id = 999999
used_ids = set()
result_df = pd.DataFrame(columns=["PaymentId", "Type", "Status"])

for _ in range(num_payments):
    payment_id = rand.randint(min_id, max_id)
    while payment_id in used_ids:
        payment_id = rand.randint(min_id, max_id)
    used_ids.add(payment_id)
    ptype = rand.choice(types)
    pstatus = rand.choice(statuses)
    result_df = result_df.append(
        {"PaymentId": payment_id, "Type": ptype, "Status": pstatus}, ignore_index=True
    )

result_df.to_csv("sample_payments.csv")
