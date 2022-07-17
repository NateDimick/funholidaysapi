# syntax=docker/dockerfile:1

FROM golang:1.18-bullseye

WORKDIR /app

COPY assets/ assets/

COPY views/ views/

COPY doc.md doc.md

COPY .env .env

ENV PORT 5000

# COPY funholidaysapi funholidaysapi # if build is a separate step then all the source doesn't have to be copied

COPY main.go main.go

COPY models/ models/

COPY mongoUtil/ mongoUtil/

COPY go.mod go.mod

COPY go.sum go.sum

RUN go mod download

RUN go build

CMD [ "./funholidaysapi" ]