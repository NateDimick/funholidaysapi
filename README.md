# fun holidays version 2

Fun holidays version 2 is built with the goals of:

1. switching from python + flask to go + gin
2. upgrading from a relational DB to MongoDB (there is nothing relational about this data)
3. updating the front end (both aesthetically to the ui and the developer)
4. a new name?

## link to a big help

[click here](https://dev.to/hackmamba/build-a-rest-api-with-golang-and-mongodb-gin-gonic-version-269m)

## API changes

1. /api/today gets new query parameters
    * tzname = string, optional, a timezone name. ex "America/New York
    * tzdelta = float, optional, difference from GMT ex 5 or 4.5
