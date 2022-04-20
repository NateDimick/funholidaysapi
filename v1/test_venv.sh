source venv/bin/activate
export FLASK_DEBUG=1
export DATABASE_URL=$(heroku config:get DATABASE_URL -a national-api-day)
flask run -h 0.0.0.0
deactivate