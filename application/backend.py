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

branch_map = {}


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
    # convert branchname to branchid
    values[1] = branch_map[values[1].lower()]
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


def delete_listing(listing, listing_type):
    tablename = get_listing_tablename(listing_type)
    id_string = "PropertyId" if listing_type == ListingType.Property else "ExperienceId"
    cur.execute(
        "DELETE FROM {0} WHERE {1} = {2};".format(tablename, id_string, listing[0])
    )


def get_listing_tablename(listing_type):
    return (
        "airbnb.property"
        if listing_type == ListingType.Property
        else "airbnb.experience"
    )


def get_branches():
    cur.execute("SELECT branchid, name from airbnb.branch")
    data = cur.fetchall()
    names = []
    for row in data:
        # mapping branchname to branchid
        branch_map[row[1].lower()] = row[0]
        names.append(row[1])
    return names
