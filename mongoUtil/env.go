package mongoUtil

import (
	"log"

	"github.com/joho/godotenv"
)

func LoadDotEnv() {
	err := godotenv.Load()
	if err != nil {
		log.Output(0, ".env load failed")
		log.Output(0, err.Error())
		log.Output(0, "assuming app is using pre-set env vars - continuing")
	}
}
