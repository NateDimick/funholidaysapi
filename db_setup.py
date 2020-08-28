"""
this script has already been run remotely to set up the heroku postgre database
TODO: set it up to delete holidays table, then reset new one
"""
import psycopg2, os
from urllib.parse import urlparse

url = urlparse(os.environ.get('DATABASE_URL'))  # export DATABASE_URL from heroku postgres sql settigns page
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(db)

cur = conn.cursor()
with open("queries/schema.sql", "r", encoding="UTF-8") as schema:
    # month,day,holiday
    cur.execute(schema.read())
with open("holiday_agg/fun_holidays.tsv", "r") as csv:
    cur.copy_from(csv, "holidays", sep="\t")
conn.commit()
cur.close()
conn.close()