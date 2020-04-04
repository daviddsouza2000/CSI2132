import psycopg2 as psy
import random as rand
from enums import *

min_id = 1000
max_id = 999999


class Backend:
    def __init__(self):
        self.conn = psy.connect(
            dbname="apoch012",
            user="apoch012",
            password="",
            port="15432",
            host="web0.eecs.uottawa.ca",
        )
        self.cur = self.conn.cursor()
        self.branch_map = {}

    def is_valid_user_id(self, user_id):
        self.cur.execute("SELECT * FROM airbnb.user WHERE userid = {0}".format(user_id))
        return len(self.cur.fetchall()) != 0

    def is_valid_employee_id(self, emp_id):
        self.cur.execute(
            "SELECT * FROM airbnb.employee WHERE employeeid = {0}".format(emp_id)
        )
        return len(self.cur.fetchall()) != 0

    def create_user(
        self,
        firstname,
        lastname,
        housenumber,
        street,
        city,
        province,
        is_super_host=False,
    ):

        user_id = rand.randint(min_id, max_id)
        self.insert(
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

    def insert(self, tablename, values, commit=True):
        SQL = "INSERT INTO " + tablename + " VALUES "

        values_template = "("
        for _ in range(len(values) - 1):
            values_template += "%s,"
        values_template += "%s)"

        args_str = self.cur.mogrify(values_template, values).decode("utf-8")
        self.cur.execute(SQL + args_str + ";")
        if commit:
            self.conn.commit()

    def insert_listing(self, listing_type, values):
        tablename = get_listing_tablename(listing_type)
        listing_id = rand.randint(min_id, max_id)
        # convert branchname to branchid
        values[1] = self.branch_map[values[1].lower()]

        amenities = []
        inclusions = []
        languages = []
        if listing_type == ListingType.Property:
            amenities = values[-1]
            values = values[:-1]
        else:
            languages = values[-1]
            inclusions = values[-2]
            values = values[:-2]

        self.insert(tablename, [listing_id] + values, commit=False)

        if len(amenities) > 0:
            for a in amenities:
                self.insert(
                    "airbnb.propertyprovidedamenities", [a, listing_id], commit=False
                )

        if len(inclusions) > 0:
            for i in inclusions:
                self.insert(
                    "airbnb.experienceinclusions", [i, listing_id], commit=False
                )

        if len(languages) > 0:
            for l in languages:
                self.insert("airbnb.experiencelanguages", [l, listing_id], commit=False)
        self.conn.commit()

    def host_select_listings(self, listing_type, host_id):
        tablename = get_listing_tablename(listing_type)
        if host_id != None:
            self.cur.execute(
                "SELECT * FROM {0} WHERE HostId = {1}".format(tablename, host_id)
            )
        else:
            self.cur.execute("SELECT * FROM {0} ".format(tablename))
        return self.cur.fetchall()

    def employee_select_listings(self, listing_type, branch_name):
        tablename = get_listing_tablename(listing_type)
        if branch_name != None:
            self.cur.execute(
                "SELECT branchid from airbnb.branch where name = %s", (branch_name,)
            )
            branch_id = self.cur.fetchall()[0][0]
            self.cur.execute(
                "SELECT * FROM {0} WHERE branchid = {1}".format(tablename, branch_id)
            )
            return self.cur.fetchall()
        else:
            self.cur.execute("SELECT * FROM {0}".format(tablename))
            return self.cur.fetchall()

    def get_all_users(self):
        self.cur.execute("SELECT * FROM airbnb.user")
        return self.cur.fetchall()

    def get_all_hosts(self, nly_super_host=False):
        if not only_super_host:
            self.cur.execute(
                """
            SELECT * FROM airbnb.user
            WHERE EXISTS(SELECT * FROM airbnb.property WHERE hostid = userid)
            OR EXISTS(SELECT * FROM airbnb.experience WHERE hostid = userid)
            """
            )
        else:
            self.cur.execute(
                """
            SELECT * FROM airbnb.user
            WHERE issuperhost = true and ( EXISTS(SELECT * FROM airbnb.property WHERE hostid = userid)
            OR EXISTS(SELECT * FROM airbnb.experience WHERE hostid = userid))
            """
            )
        return self.cur.fetchall()

    def update_listing(self, listing_type, listing, attrib, value):
        tablename = get_listing_tablename(listing_type)
        id_string = (
            "PropertyId" if listing_type == ListingType.Property else "ExperienceId"
        )
        self.cur.execute(
            "UPDATE {0} SET {1} = %s  WHERE {2} = {3}".format(
                tablename, attrib, id_string, listing[0]
            ),
            (value,),
        )
        self.conn.commit()

    def delete_listing(self, listing, listing_type):
        tablename = get_listing_tablename(listing_type)
        id_string = (
            "PropertyId" if listing_type == ListingType.Property else "ExperienceId"
        )
        self.cur.execute(
            "DELETE FROM {0} WHERE {1} = {2};".format(tablename, id_string, listing[0])
        )
        self.conn.commit()

    def create_booking(self, listing_type, inputs):
        booking_tablename = get_booking_tablename(listing_type)
        booking_id = rand.randint(min_id, max_id)
        self.insert(booking_tablename, [booking_id] + inputs)
        return booking_id

    def create_payment(self, booking_id, prop_exp_id, payment_type, listing_type):
        payment_id = rand.randint(min_id, max_id)
        self.insert("airbnb.payment", [payment_id, payment_type, "completed"])
        tablename = (
            "airbnb.propertypayments"
            if listing_type == ListingType.Property
            else "airbnb.experiencepayments"
        )
        self.insert(tablename, [payment_id, prop_exp_id, booking_id])
        self.conn.commit()

    def get_listing_bookings(self, listing, listing_type):
        booking_tablename = get_booking_tablename(listing_type)
        id_string = (
            "PropertyId" if listing_type == ListingType.Property else "ExperienceId"
        )
        self.cur.execute(
            "SELECT * FROM {0} WHERE {1} = {2}".format(
                booking_tablename, id_string, listing[0]
            )
        )
        return self.cur.fetchall()

    def get_user_bookings(self, listing_type, user_id):
        booking_tablename = get_booking_tablename(listing_type)
        self.cur.execute(
            "SELECT * FROM {0} WHERE userid = {1}".format(booking_tablename, user_id)
        )
        return self.cur.fetchall()

    def delete_booking(self, booking, listing_type):
        booking_tablename = get_booking_tablename(listing_type)
        self.cur.execute(
            "DELETE FROM {0} WHERE bookingid = {1};".format(
                booking_tablename, booking[0]
            )
        )
        self.conn.commit()

    def get_branches(self):
        self.cur.execute("SELECT branchid, name from airbnb.branch")
        data = self.cur.fetchall()
        names = []
        for row in data:
            # mapping branchname to branchid
            self.branch_map[row[1].lower()] = row[0]
            names.append(row[1])
        return names

    def get_unavailable_intervals(self, listing, listing_type):
        booking_tablename = get_booking_tablename(listing_type)
        id_string = (
            "PropertyId" if listing_type == ListingType.Property else "ExperienceId"
        )
        self.cur.execute(
            "SELECT StartDateTime, EndDateTime FROM {0} WHERE {1} = {2}".format(
                booking_tablename, id_string, listing[0]
            )
        )
        return self.cur.fetchall()

    def get_property_amenities(self, property_id):
        self.cur.execute(
            "SELECT amenityname from airbnb.propertyprovidedamenities where propertyid = {0}".format(
                property_id
            )
        )
        return self.cur.fetchall()

    def get_experience_inclusions(self, experience_id):
        self.cur.execute(
            "SELECT inclusionname from airbnb.experienceinclusions where experienceid = {0}".format(
                experience_id
            )
        )
        return self.cur.fetchall()

    def get_experience_languages(self, experience_id):
        self.cur.execute(
            "SELECT languagename from airbnb.experiencelanguages where experienceid = {0}".format(
                experience_id
            )
        )
        return self.cur.fetchall()

    def get_amenities(self):
        self.cur.execute("SELECT * from airbnb.amenity")
        return self.cur.fetchall()

    def get_inclusions(self):
        self.cur.execute("SELECT * from airbnb.inclusion")
        return self.cur.fetchall()

    def get_languages(self):
        self.cur.execute("SELECT * from airbnb.language")
        return self.cur.fetchall()

    def get_week_experience_listings(self):
        self.cur.execute(
            """
            select * from airbnb.experience 
            where experienceid in (
                    select experienceid from airbnb.experiencebooking
                    where startdatetime > NOW() and startdatetime < (NOW() + interval '1 week')
            );
        """
        )
        return self.cur.fetchall()

    def get_week_property_listings(self):
        self.cur.execute(
            """
                select * from airbnb.property 
                where propertyid in (
                        select propertyid from airbnb.propertybooking
                        where startdatetime > NOW() and startdatetime < (NOW() + interval '1 week')
                );
                """
        )
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.close()


def get_listing_tablename(listing_type):
    return (
        "airbnb.property"
        if listing_type == ListingType.Property
        else "airbnb.experience"
    )


def get_booking_tablename(listing_type):
    return (
        "airbnb.propertybooking"
        if listing_type == ListingType.Property
        else "airbnb.experiencebooking"
    )
