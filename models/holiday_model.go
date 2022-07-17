package models

import (
	"funholidaysapi/mongoUtil"
	"log"

	"go.mongodb.org/mongo-driver/mongo"
)

type DayHolidayMap map[int][]string

// for searchQUery
type MonthDayMap map[int]DayHolidayMap

// for the random endpoint - just a single holiday and its date
// also a representation of each holiday document in mongo
type Holiday struct {
	Name  string `json:"holiday"`
	Month int    `json:"month"`
	Day   int    `json:"day"`
}

// used for dateQuery, today
type HoidayDayList struct {
	Names []string `json:"holidays"`
	Month int      `json:"month"`
	Day   int      `json:"day"`
}

// for monthQuery
type HolidayMonthList struct {
	Month    int           `json:"month"`
	Holidays DayHolidayMap `json:"holidays"`
}

// TODO all of these
func DayListFromResults(resultSet *mongo.Cursor) (*HoidayDayList, error) {
	resultList := HoidayDayList{Names: []string{}}
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	for resultSet.Next(ctx) {
		var holiday Holiday
		err := resultSet.Decode(&holiday)
		if err != nil {
			log.Fatal("could not decode item to Holiday")
			log.Fatal(err.Error())
			return nil, err
		}
		resultList.Names = append(resultList.Names, holiday.Name)
		resultList.Day = holiday.Day
		resultList.Month = holiday.Month
	}
	return &resultList, nil
}

func MonthListFromResults(resultSet *mongo.Cursor) (*HolidayMonthList, error) {
	resultObj := HolidayMonthList{Holidays: make(DayHolidayMap)}
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	for resultSet.Next(ctx) {
		var holiday Holiday
		err := resultSet.Decode(&holiday)
		if err != nil {
			log.Fatal("could not decode item to Holiday")
			log.Fatal(err.Error())
			return nil, err
		}
		resultObj.Month = holiday.Month
		resultObj.Holidays[holiday.Day] = append(resultObj.Holidays[holiday.Day], holiday.Name)
	}
	return &resultObj, nil
}

func SearchResultsFromResults(resultSet *mongo.Cursor) (*MonthDayMap, error) {
	resultObj := make(MonthDayMap)
	ctx, cancelFunc := mongoUtil.Timeout()
	defer cancelFunc()
	for resultSet.Next(ctx) {
		var holiday Holiday
		err := resultSet.Decode(&holiday)
		if err != nil {
			log.Fatal("could not decode item to Holiday")
			log.Fatal(err.Error())
			return nil, err
		}
		if resultObj[holiday.Month] == nil {
			resultObj[holiday.Month] = make(DayHolidayMap)
		}
		resultObj[holiday.Month][holiday.Day] = append(resultObj[holiday.Month][holiday.Day], holiday.Name)
	}
	return &resultObj, nil
}
