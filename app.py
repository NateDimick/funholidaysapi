import datetime, json, psycopg2, os, random, markdown
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify
from flask_api import status
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
url = urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(db)

cur = conn.cursor()
month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

@app.route("/")
def index():
    h = today().json
    return render_template("index.html", month=h['month'], day = h['day'], holidays=h['holidays'])


@app.route("/api")
def docs():
    with open("README.md", 'r', encoding="UTF-8") as f:
        i = f.read()
        readme = markdown.markdown(i, extensions=["fenced_code"])
    return render_template("docs.html", md=readme)

@app.route("/app")
def lookup():
    return render_template("lookup.html")


def holidays_date(month, day):
    if not 1 <= month <= 12:
        return {}
    else:
        if not 1 <= day <= month_days[month - 1]:
            return {}
    with open("queries/date.sql", "r") as query:
        cur.execute(query.read(), (month, day))
        holidays = cur.fetchall()
        return holidays


# actual api routes
@app.route("/api/today")
def today():
    """
    returns all of the fun holidays that are today
    """
    today = datetime.date.today()
    day = today.day
    month = today.month
    holidays = holidays_date(month, day)

    return jsonify({"day": day, "month": month, "holidays": [h[0] for h in holidays]})

@app.route("/api/month")
def month():
    """
    returns all of the fun holidays the specified month
    """
    m = int(request.args.get("month", 0))
    if not 1 <= m <= 12:
        # throw error
        return jsonify({}), status.HTTP_400_BAD_REQUEST
    with open("queries/month.sql", "r") as query:
        cur.execute(query.read(), (m, ))
        holidays = cur.fetchall()

    this_month = {}
    for h in holidays:
        this_month[h[0]] = this_month.get(h[0], []) + [h[1]]

    return jsonify({"month": m, "holidays": this_month})

@app.route("/api/date")
def date():
    """
    returns all the fun holidays on the specified date
    """
    month = int(request.args.get("month", 0))
    day = int(request.args.get("day", 0))
    holidays = holidays_date(month, day)
    if not holidays:
        return jsonify(holidays), status.HTTP_400_BAD_REQUEST

    return jsonify({"day": day, "month": month, "holidays": [h[0] for h in holidays]})

@app.route("/api/when")
def when():
    """
    returns the names and dates of holidays that match a query string
    """
    pattern = request.args.get("like", "") # TODO: make sure this is safe from injection attacks
    if not pattern:
        # throw error
        return jsonify({}), status.HTTP_400_BAD_REQUEST
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

    return jsonify(days)

@app.route("/api/random")
def rand_holiday():
    month = random.randint(1, 12)
    day = random.randint(1, month_days[month - 1])
    holidays = holidays_date(month, day)
    random.shuffle(holidays)
    winner = holidays[0]
    h = winner[0]
    return jsonify({"month": month, "day": day, "holiday": h})


# use flask run -h 0.0.0.0
# also export FLASK_DEBUG=1
#app.run(debug=True,host='0.0.0.0')