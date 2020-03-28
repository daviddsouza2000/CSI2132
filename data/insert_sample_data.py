import psycopg2 as psy

conn = psy.connect(dbname = "apoch012", user ="apoch012", password = "3I6WjM8eWUo&", port = "15432",
        host = "web0.eecs.uottawa.ca")

print(conn)

