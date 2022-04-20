import datetime
from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import random

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


def holidays_date(month, day):
    if not 1 <= month <= 12:
        return {}
    else:
        if not 1 <= day <= month_days[month - 1]:
            return {}
    return Holidays.query.filter_by(month=month, day=day).all()


# actual api routes
# TODO: surround with try/catch in real deploy so flask error pages don't show up
@app.route("/today")
def today():
    """
    returns all of the fun holidays that are today
    """
    request_today = request.date
    today = datetime.date.today()
    print(request.headers, request.url)
    print(request_today)
    print(today)
    day = today.day
    month = today.month
    holidays = holidays_date(month, day)

    return jsonify({"day": day, "month": month, "holidays": [h.holiday for h in holidays]})

@app.route("/month/<int:m>")
def month(m=0):
    """
    returns all of the fun holidays the specified month
    """
    if not 1 <= m <= 12:
        # throw error
        return jsonify({}), status.HTTP_400_BAD_REQUEST
    holidays = Holidays.query.filter_by(month=m).all()

    this_month = {}
    for h in holidays:
        this_month[h.day] = this_month.get(h.day, []) + [h.holiday]

    return jsonify({"month": m, "holidays": this_month})

@app.route("/date/<int:m>/<int:d>")
def date(m=0,d=0):
    """
    returns all the fun holidays on the specified date
    """
    holidays = holidays_date(m, d)
    if not holidays:
        return jsonify(holidays), status.HTTP_400_BAD_REQUEST

    return jsonify({"day": d, "month": m, "holidays": [h.holiday for h in holidays]})

@app.route("/search/<pattern>")
def when(pattern):
    """
    returns the names and dates of holidays that match a query string
    """
    
    if not pattern:
        # throw error
        return jsonify({}), status.HTTP_400_BAD_REQUEST
    holidays = Holidays.query.filter(Holidays.holiday.ilike(f"%{pattern}%")).all()

    days = {}
    for h in holidays:
        m = days.get(h.month, {})  # creates new month dict if first time
        d = m.get(h.day, [])     # creates new day list if first time
        d.append(h.holiday)          # append holiday 
        m[h.day] = d             # replace day list (or assign it)
        days[h.month] = m          # replace (or assign) month dict

    return jsonify(days)

@app.route("/random")
def rand_holiday():
    month = random.randint(1, 12)
    day = random.randint(1, month_days[month - 1])
    holidays = holidays_date(month, day)
    random.shuffle(holidays)
    winner = holidays[0]
    return jsonify({"month": month, "day": day, "holiday": winner.holiday})