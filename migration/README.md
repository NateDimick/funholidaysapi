# migration

this is just a quick one-off script to migrate existing data from heroku postgres to new mongoDB via the existing v1 API.

cd to this directory and `go run migration.go` to copy from my DB to yours.

this could probably be multithreaded and better written but it's not.

things that could make this better:

* bulk inserts
* goroutines/multithreading

took about 7 minutes to run w/ 7470 documents on an i5 laptop processor
