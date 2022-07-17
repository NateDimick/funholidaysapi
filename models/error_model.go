package models

type ErrorResponse struct {
	ErrorDescription string `json:"error"`
	ErrorDetails     string `json:"detail"`
}
