package mongoUtil

import (
	"context"
	"log"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var database string = "MONGODBNAME"
var mongouri string = "MONGOURI"

func Connect() *mongo.Client {
	client, err := mongo.NewClient(options.Client().ApplyURI(os.Getenv(mongouri)))
	if err != nil {
		log.Fatal(err.Error())
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err.Error())
	}

	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatal(err.Error())
	}

	log.Print("mongoDb connection complete")
	return client
}

func GetCollection(client *mongo.Client, collectionName string) *mongo.Collection {
	collection := client.Database(os.Getenv(database)).Collection(collectionName)
	return collection
}
