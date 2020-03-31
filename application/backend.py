import psycopg2 as psy
import random as rand

conn = psy.connect(
    dbname="apoch012",
    user="apoch012",
    password="&",
    port="15432",
    host="web0.eecs.uottawa.ca",
)

cur = conn.cursor()


def create_user(
    firstname, lastname, housenumber, street, city, province, is_super_host=False
):
    min_id = 1000
    max_id = 999999

    user_id = rand.randint(min_id, max_id)
    insert(
        "airbnb.user",
        [
            user_id,
            firstname,
            lastname,
            housenumber,
            street,
            city,
            province,
            is_super_host,
        ],
    )
    return user_id


def insert(tablename, values):
    SQL = "INSERT INTO " + tablename + " VALUES "

    values_template = "("
    for _ in range(len(values) - 1):
        values_template += "%s,"
    values_template += "%s)"

    args_str = cur.mogrify(values_template, values).decode("utf-8")
    cur.execute(SQL + args_str + ";")
    conn.commit()
