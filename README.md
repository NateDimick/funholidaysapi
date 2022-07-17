# fun holidays version 2

Fun holidays version 2 is built with the goals of:

1. switching from python + flask to go + gin [success]
2. upgrading from a relational DB to MongoDB (there is nothing relational about this data) [success]
3. updating the front end (both aesthetically to the ui and the developer) [TBD]
4. a new name? [TBD]

## link to a big help

[click here](https://dev.to/hackmamba/build-a-rest-api-with-golang-and-mongodb-gin-gonic-version-269m)

## API changes

* may not actually be implemented yet

1. /api/today gets new query parameters
    * tzname = string, optional, a timezone name. ex "America/New York
    * tzdelta = float, optional, difference from GMT ex 5 or 4.5

## Docker

Just like a late version of v1, this is app is ready to be containerized. if you want to run locally, but first you need to populate a `.env` file. see `.env-example` for what values are required. Alternatively, the env variables could be places directly in the environment/docker file
