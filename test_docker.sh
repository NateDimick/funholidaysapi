export DOCKER_BUILDKIT=1
export DATABASE_URL=$(heroku config:get DATABASE_URL -a national-api-day)
sudo docker build --tag national-api-day --build-arg DB=$DATABASE_URL .
sudo docker run --publish 5000:5000 national-api-day