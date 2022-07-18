package main

import (
	"fmt"
	"funholidaysapi/models"
	"funholidaysapi/mongoUtil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/gomarkdown/markdown"

	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var mongoClient *mongo.Client
var holidayCollection *mongo.Collection

func today(c *gin.Context) {
	currentTime := time.Now()
	_, month, dayNum := currentTime.Date()
	fmt.Printf("today is %d/%d", month, dayNum)
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	resultSet, err := holidayCollection.Find(ctx, bson.M{"month": month, "day": dayNum})
	if err != nil {
		// return 500
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{ErrorDescription: "oops. maybe there's no holidays today", ErrorDetails: err.Error()})
		return
	}
	responseBody, err := models.DayListFromResults(resultSet)
	c.JSON(http.StatusOK, responseBody)
	return

}

func monthQuery(c *gin.Context) {
	monthNum, err := strconv.Atoi(c.Param("monthNum"))
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{ErrorDescription: "oops. gotta be a number, dude", ErrorDetails: err.Error()})
		return
	}
	fmt.Printf("finding all holidays in month #%d", monthNum)
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	resultSet, err := holidayCollection.Find(ctx, bson.M{"month": monthNum})
	if err != nil {
		// return 500
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{ErrorDescription: "oops. maybe there's no holidays that month", ErrorDetails: err.Error()})
		return
	}
	responseBody, err := models.MonthListFromResults(resultSet)
	c.JSON(http.StatusOK, responseBody)
	return

}

func dateQuery(c *gin.Context) {
	monthNum, err := strconv.Atoi(c.Param("monthNum"))
	dayNum, err := strconv.Atoi(c.Param("dayNum"))
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{ErrorDescription: "oops. gotta be a number, dude", ErrorDetails: err.Error()})
		return
	}
	fmt.Printf("finding all holidays on %d/%d", monthNum, dayNum)
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	resultSet, err := holidayCollection.Find(ctx, bson.M{"month": monthNum, "day": dayNum})
	if err != nil {
		// return 500
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{ErrorDescription: "oops. maybe there's no holidays on that date", ErrorDetails: err.Error()})
		return
	}
	responseBody, err := models.DayListFromResults(resultSet)
	c.JSON(http.StatusOK, responseBody)
	return
}

func searchQuery(c *gin.Context) {
	keyword := c.Param("keyword")
	fmt.Printf("finding all %s holidays", keyword)
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	resultSet, err := holidayCollection.Find(ctx, bson.M{"name": primitive.Regex{Pattern: fmt.Sprintf(".*%s.*", keyword), Options: "i"}})
	if err != nil {
		// return 500
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{ErrorDescription: "oops. maybe there's no holidays on that date", ErrorDetails: err.Error()})
		return
	}
	if resultSet.RemainingBatchLength() == 0 {
		log.Print("no search results")
	}
	responseBody, err := models.SearchResultsFromResults(resultSet)
	c.JSON(http.StatusOK, responseBody)
	return

}

func randomHoliday(c *gin.Context) {
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	daysPerMonth := []int{31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
	monthNum := rand.Int() % 12
	dayNum := rand.Int() % daysPerMonth[monthNum]
	filter := bson.M{"month": monthNum + 1, "day": dayNum}
	maxRand, err := holidayCollection.CountDocuments(ctx, filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{ErrorDescription: "oops. not good at counting", ErrorDetails: err.Error()})
		return
	}
	choice := rand.Int() % int(maxRand)
	cur, err := holidayCollection.Find(ctx, filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{ErrorDescription: "oops. couldn't pick a card, any card", ErrorDetails: err.Error()})
		return
	}
	for i := 0; i < choice; i++ {
		cur.Next(ctx)
	}
	var selection models.Holiday
	cur.Decode(&selection)
	c.JSON(http.StatusOK, selection)
	return

}

func renderIndex(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", gin.H{
		"title": "National Api Day",
	})
}

func renderDemo(c *gin.Context) {
	keyword := c.Query("kw")
	date := c.Query("dt")
	c.HTML(http.StatusOK, "lookup", gin.H{
		"title":   "Fun Holiday Lookup Tool",
		"date":    func() string { return date },
		"keyword": func() string { return keyword },
	})
}

func renderDocs(c *gin.Context) {
	//read file
	md, err := os.ReadFile("doc.md")
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{ErrorDescription: "oops. reading markdown is hard", ErrorDetails: err.Error()})
		return
	}
	// parse markdown
	mdAsHtml := markdown.ToHTML(md, nil, nil)
	c.Data(http.StatusOK, "text/html; charset=utf-8", mdAsHtml)
}

func main() {
	fmt.Println("running gin app holiday api")
	mongoUtil.LoadDotEnv()
	mongoClient = mongoUtil.Connect()
	ctx, cancelFunc := mongoUtil.Timeout()
	defer mongoClient.Disconnect(ctx)
	defer cancelFunc()
	holidayCollection = mongoUtil.GetCollection(mongoClient, os.Getenv("HOLIDAYCOLLECTIONNAME"))

	r := gin.Default()
	api := r.Group("/api")
	{
		api.GET("/today", today)
		api.GET("/month/:monthNum", monthQuery)
		api.GET("/date/:monthNum/:dayNum", dateQuery)
		api.GET("/search/:keyword", searchQuery)
		api.GET("/random", randomHoliday)
	}

	r.GET("/", renderIndex)

	r.GET("/raw-docs", renderDocs)

	r.LoadHTMLGlob("frontendV2/public/*.html")

	r.Static("/assets", "./frontendV2/public")

	r.Run()
}
