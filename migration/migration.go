package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"funholidaysapi/models"
	"funholidaysapi/mongoUtil"

	"go.mongodb.org/mongo-driver/mongo"
)

func GetCollection(client *mongo.Client) *mongo.Collection {
	collection := client.Database(os.Getenv("MONGODBNAME")).Collection(os.Getenv("HOLIDAYCOLLECTIONNAME"))
	return collection
}

func main() {
	fmt.Println("moving data from old api to mongo")
	mongoUtil.LoadDotEnv()
	mongoClient := mongoUtil.Connect()
	holidayCollection := GetCollection(mongoClient)
	const url string = "https://national-api-day.herokuapp.com/api/month/%d"
	migrationCount := 0
	for i := 1; i < 13; i++ {
		resp, err := http.Get(fmt.Sprintf(url, i))
		fmt.Println("getting month")
		if err != nil {
			fmt.Printf("could not get month %d", i)
			continue
		}
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			fmt.Printf("could not read response body %d \n", i)
			continue
		}
		var usableResponse models.HolidayMonthList
		err = json.Unmarshal(body, &usableResponse)
		if err != nil {
			fmt.Println("couldn't unmarshal binary response body")
			fmt.Println(err.Error())
		}
		//fmt.Print(usableResponse)
		for day, holidayList := range usableResponse.Holidays {
			for _, holiday := range holidayList {
				document := models.Holiday{Day: day, Name: holiday, Month: usableResponse.Month}
				ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
				defer cancel()
				_, err := holidayCollection.InsertOne(ctx, document)
				if err != nil {
					fmt.Println("insert error")
					fmt.Println(err.Error())
					return
				}
				migrationCount++
			}
		}
	}
	fmt.Println("migration complete")
	fmt.Printf("%d documents migrated", migrationCount)
}
