package mongoUtil

import (
	"context"
	"time"
)

func Timeout() (context.Context, context.CancelFunc) {
	return context.WithTimeout(context.Background(), 10*time.Second)
}
