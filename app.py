import datetime, json, psycopg2, os
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)
url = urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(db)

cur = conn.cursor()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api")
def docs():
    return render_template("docs.html")

# actual api routes
@app.route("/api/today")
def today():
    """
    returns all of the fun holidays that are today
    """
    today = datetime.date.today()
    day = today.day
    month = today.month
    with open("queries/date.sql", "r") as query:
        cur.execute(query.read(), (month, day))
        holidays = cur.fetchall()

    return json.dumps({"day": day, "month": month, "holidays": [h[0] for h in holidays]})

@app.route("/api/month")
def month():
    """
    returns all of the fun holidays the specified month
    """
    m = int(request.args.get("month", 0))
    if not m:
        # throw error
        pass
    with open("queries/month.sql", "r") as query:
        cur.execute(query.read(), (str(m)))
        holidays = cur.fetchall()

    this_month = {}
    for h in holidays:
        this_month[h[0]] = this_month.get(h[0], []) + [h[1]]

    return json.dumps({"month": m, "holidays": this_month})

@app.route("/api/date")
def date():
    """
    returns all the fun holidays on the specified date
    """
    month = int(request.args.get("month", 0))
    day = int(request.args.get("day", 0))
    if not month or not day:
        # throw error
        pass
    with open("queries/date.sql", "r") as query:
        cur.execute(query.read(), (month, day))
        holidays = cur.fetchall()

    return json.dumps({"day": day, "month": month, "holidays": [h[0] for h in holidays]})

@app.route("/api/when")
def when():
    """
    returns the names and dates of holidays that match a query string
    """
    pattern = request.args.get("like", "") # TODO: make sure this is safe from injection attacks
    if not pattern:
        # throw error
        pass
    with open("queries/when.sql", "r") as query:
        cur.execute(query.read(), (f"%{pattern}%", ))
        holidays = cur.fetchall()

    days = {}
    print(pattern, holidays)
    for h in holidays:
        m = days.get(h[0], {})  # creates new month dict if first time
        d = m.get(h[1], [])     # creates new day list if first time
        d.append(h[2])          # append holiday 
        m[h[1]] = d             # replace day list (or assign it)
        days[h[0]] = m          # replace (or assign) month dict

    return json.dumps(days)





#app.run(debug=True,host='0.0.0.0')