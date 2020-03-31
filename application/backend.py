import psycopg2 as psy
import random as rand
from enums import *

conn = psy.connect(
    dbname="apoch012",
    user="apoch012",
    password="",
    port="15432",
    host="web0.eecs.uottawa.ca",
)

cur = conn.cursor()

min_id = 1000
max_id = 999999


def create_user(
    firstname, lastname, housenumber, street, city, province, is_super_host=False
):

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


def insert_listing(listing_type, values):
    tablename = get_listing_tablename(listing_type)
    listing_id = rand.randint(min_id, max_id)
    insert(tablename, [listing_id] + values)


def host_select_listings(listing_type, host_id):
    tablename = get_listing_tablename(listing_type)
    cur.execute("SELECT * FROM {0} WHERE HostId = {1}".format(tablename, host_id))
    return cur.fetchall()


def update_listing(listing_type, listing, attrib, value):
    tablename = get_listing_tablename(listing_type)
    id_string = "PropertyId" if listing_type == ListingType.Property else "ExperienceId"
    cur.execute(
        "UPDATE {0} SET {1} = %s  WHERE {2} = {3}".format(
            tablename, attrib, id_string, listing[0]
        ),
        (value,),
    )
    conn.commit()


def get_listing_tablename(listing_type):
    return (
        "airbnb.property"
        if listing_type == ListingType.Property
        else "airbnb.experience"
    )
