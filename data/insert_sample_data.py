import psycopg2 as psy

conn = psy.connect(
    dbname="apoch012",
    user="apoch012",
    password="3I6WjM8eWUo&",
    port="15432",
    host="web0.eecs.uottawa.ca",
)

# allows interaction with database
cur = conn.cursor()

""" 
>>> SQL = 'INSERT INTO authors (name) VALUES (%s);' # Note: no quotes
>>> data = ('OReilly', )
>>> cur.execute(SQL, data) # Note: no % operator
"""

info = [
    ("sample_users.csv", "airbnb.user"),
    ("sample_branches.csv", "airbnb.branch"),
    ("sample_employees.csv", "airbnb.employee"),
    ("sample_properties_clean.csv", "airbnb.property"),
    ("sample_experiences.csv", "experience"),
    ("sample_amenities.csv", "airbnb.amenity"),
    ("sample_languages.csv", "airbnb.language"),
    ("sample_inclusions.csv", "airbnb.inclusions"),
    ("sample_property_amenities.csv", "airbnb.propertyprovidedamenities"),
    ("sample_experience_languages.csv", "airbnb.experiencelanguages"),
    ("sample_experience_inclusions.csv", "airbnb.experienceinclusions"),
    ("sample_property_bookings.csv", "airbnb.propertybooking"),
    ("sample_experience_bookings.csv", "airbnb.experiencebooking"),
    ("sample_payments.csv", "airbnb.payment"),
    ("sample_property_payments.csv", "airbnb.propertypayments"),
    ("sample_experience_payments.csv", "airbnb.experiencepayments"),
    ("sample_prop_review.csv", "airbnb.propertyreview"),
    ("sample_exp_reviews.csv", "airbnb.experiencereview"),
    ("sample_email.csv", "airbnb.emailaddresss"),
    ("sample_phonenumbers.csv", "airbnb.phonenumber"),
]
