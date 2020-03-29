import pandas as pd
import numpy
import psycopg2 as psy


def insert_data(info, cur):
    filename = info[0]
    tablename = info[1]
    df = pd.read_csv(filename)
    df.drop(df.filter(regex="Unname"), axis=1, inplace=True)
    SQL = "INSERT INTO " + tablename + " VALUES "

    values_template = "("
    num_cols = len(df.columns)
    for _ in range(num_cols - 1):
        values_template += "%s,"
    values_template += "%s)"

    for _, row in df.iterrows():
        data = []
        columns = []
        cols_str = "("
        for col in df:
            if type(row[col]) is numpy.int64:
                data.append(int(row[col]))
            else:
                data.append(row[col])

            columns.append(col)
            cols_str += col + ","

        cols_str = cols_str[:-1] + ")"
        # this is because employee doesnt exist yet so we can't provide a FK to the manager yet
        if tablename == "airbnb.branch":
            data[1] = None

        if tablename == "airbnb.phonenumber":
            data[0] = str(data[0])

        args_str = cur.mogrify(values_template, data).decode("utf-8")

        cur.execute("INSERT INTO " + tablename + cols_str + " VALUES " + args_str + ";")


conn = psy.connect(
    dbname="apoch012",
    user="apoch012",
    password="3I6WjM8eWUo&",
    port="15432",
    host="web0.eecs.uottawa.ca",
)

# allows interaction with database
cur = conn.cursor()

info_list = [
    ("sample_users.csv", "airbnb.user"),
    ("sample_phonenumbers.csv", "airbnb.phonenumber"),
    ("sample_branches.csv", "airbnb.branch"),
    ("sample_employees.csv", "airbnb.employee"),
    ("sample_properties_clean.csv", "airbnb.property"),
    ("sample_experiences.csv", "airbnb.experience"),
    ("sample_amenities.csv", "airbnb.amenity"),
    ("sample_languages.csv", "airbnb.language"),
    ("sample_inclusions.csv", "airbnb.inclusion"),
    ("sample_experience_languages.csv", "airbnb.experiencelanguages"),
    ("sample_experience_inclusions.csv", "airbnb.experienceinclusions"),
    ("sample_property_bookings.csv", "airbnb.propertybooking"),
    ("sample_experience_bookings.csv", "airbnb.experiencebooking"),
    ("sample_payments.csv", "airbnb.payment"),
    ("sample_property_payments.csv", "airbnb.propertypayments"),
    ("sample_experience_payments.csv", "airbnb.experiencepayments"),
    ("sample_prop_reviews.csv", "airbnb.propertyreview"),
    ("sample_exp_reviews.csv", "airbnb.experiencereview"),
    ("sample_email.csv", "airbnb.emailaddress"),
    ("sample_property_amenities.csv", "airbnb.propertyprovidedamenities"),
]

for info in info_list:
    insert_data(info, cur)
    print("done for ", info[1])

branch_df = pd.read_csv("sample_branches.csv")
for _, b in branch_df.iterrows():
    cur.execute(
        "UPDATE airbnb.branch SET managerid = {0} WHERE branchid = {1}".format(
            b["ManagerId"], b["BranchId"]
        )
    )
conn.commit()
