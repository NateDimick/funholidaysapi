import datetime, json, os, random, markdown
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify
from flask_api import status
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'makeNewKeyLater'
db = SQLAlchemy(app)

month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# TODO: mode to own file?
class Holidays(db.Model):
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    holiday = db.Column(db.String(255), primary_key=True) #, unique=True)
    # source = db.Column(db.String(255))
    # last_updated = db.Column(db.String(255))
    # fixed_date = db.Column(db.Boolean())

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
    args = request.args        
    if args.get("kw", ""):
        return render_template("lookup.html", keyword=args["kw"])
    elif args.get("dt", ""):
        return render_template("lookup.html", date=args["dt"])
    else:
        return render_template("lookup.html")



def holidays_date(month, day):
    if not 1 <= month <= 12:
        return {}
    else:
        if not 1 <= day <= month_days[month - 1]:
            return {}
    return Holidays.query.filter_by(month=month, day=day).all()


# actual api routes
# TODO: surround with try/catch in real deploy so flask error pages don't show uuuuuuuuuu
@app.route("/api/today")
def today():
    """
    returns all of the fun holidays that are today
    """
    today = datetime.date.today()
    day = today.day
    month = today.month
    holidays = holidays_date(month, day)
    print(holidays)

    return jsonify({"day": day, "month": month, "holidays": [h.holiday for h in holidays]})

@app.route("/api/month/<m>")
def month(m=0):
    """
    returns all of the fun holidays the specified month
    """
    m = int(m)
    if not 1 <= m <= 12:
        # throw error
        return jsonify({}), status.HTTP_400_BAD_REQUEST
    holidays = Holidays.query.filter_by(month=m).all()

    this_month = {}
    for h in holidays:
        this_month[h.day] = this_month.get(h.day, []) + [h.holiday]

    return jsonify({"month": m, "holidays": this_month})

@app.route("/api/date/<m>/<d>")
def date(m=0,d=0):
    """
    returns all the fun holidays on the specified date
    """
    month = int(m)
    day = int(d)
    holidays = holidays_date(month, day)
    if not holidays:
        return jsonify(holidays), status.HTTP_400_BAD_REQUEST

    return jsonify({"day": day, "month": month, "holidays": [h.holiday for h in holidays]})

@app.route("/api/when")
def when():
    """
    returns the names and dates of holidays that match a query string
    """
    pattern = request.args.get("like", "") # TODO: make sure this is safe from injection attacks
    if not pattern:
        # throw error
        return jsonify({}), status.HTTP_400_BAD_REQUEST
    holidays = Holidays.query.filter(Holidays.holiday.ilike(f"%{pattern}%")).all()

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
    return jsonify({"month": month, "day": day, "holiday": winner.holiday})


# use flask run -h 0.0.0.0
# also export FLASK_DEBUG=1
#app.run(debug=True,host='0.0.0.0')