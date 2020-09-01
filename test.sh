source venv/bin/activate
export FLASK_DEBUG=1
export DATABASE_URL=$(heroku config:get DATABASE_URL -a fun-holiday-api)
flask run -h 0.0.0.0
deactivate
