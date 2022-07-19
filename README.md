# fun holidays version 2

## About the App

This app is built on top of a web-scraped collection of "official holidays" that are accurate as of 2020.

## Technology used

The stack of this app's previous version was:

* Python
* Flask
* Jinja rendered templates for frontend UI
* PostgreSQL

The new stack is:

* Go
* Gin
* Svelte
* MongoDB

## Why rebuild?

1. Learning new languages and frameworks is fun and cool
2. Provides an opportunity to revisit and old project and make it better
3. The data was not relational (a single table), a document store makes more sense for this application vs a relational database.
4. Smaller Docker image - V1 was about 160 MB, v2 is around 25 MB
5. I wanted to and that should be good enough

## How Gin + Svelte work together

Svelte is a compiler framework, not a runtime framework. This means we can build our frontend framework, and then serve it as static files. Gin makes it easy to serve static files like this:

``` go
// code is from main.go
func renderIndex(c *gin.Context) {
    c.HTML(http.StatusOK, "index.html", gin.H{
        "title": "National Api Day",
    })
}

r.GET("/", renderIndex)

r.LoadHTMLGlob("frontendV2/public/*.html") // allows renderIndex to find index.html

r.Static("/assets", "./frontendV2/public") // maps any URL path that starts with /assets/ to map to the local /frontendV2/public directory
```

The frontend uses the [svelte-spa-router](https://github.com/ItalyPaleAle/svelte-spa-router) to create a single page application. This way, our backend only has to serve one static html file.

The frontend and backend are build in stages in a Docker environment with an alpine linux final stage so the entire app can be run and served from anywhere.

## link to a big help

[click here](https://dev.to/hackmamba/build-a-rest-api-with-golang-and-mongodb-gin-gonic-version-269m)

## API changes

* may not actually be implemented yet

1. #/api/today gets new query parameters
    * tzname = string, optional, a timezone name. ex "America/New York"
    * tzdelta = float, optional, difference from GMT ex 5 or 4.5

## Docker

Just like a late version of v1, this is app is ready to be containerized. Two Dockerfiles are included and the only real difference between them is how they handle environment variables.

* `Dockerfile` is intended for local development where you can safely create and populate a `.env` file in the root fo the project directory. It will copy that .env file and the backend executable will load it upon startup.
* `Dockerfile-Heroku` is used for Heroku deploys where environment variables are kept secret with config vars (or another provider's equivalent) and are passed in to the container at runtime.
