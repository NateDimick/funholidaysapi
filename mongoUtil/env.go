package mongoUtil

import (
	"log"

	"github.com/joho/godotenv"
)

func LoadDotEnv() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal(".env load failed")
		log.Fatal(err.Error())
	}
}
