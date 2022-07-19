# syntax=docker/dockerfile:1

FROM node:18-bullseye

WORKDIR /frontend

COPY frontendV2/ ./

RUN npm install

RUN npm run build

FROM golang:1.18-bullseye

WORKDIR /backend

# COPY funholidaysapi funholidaysapi # if build is a separate step then all the source doesn't have to be copied

COPY main.go go.sum go.mod ./

COPY models/ models/

COPY mongoUtil/ mongoUtil/

RUN go mod download

RUN CGO_ENABLED=0 go build

# this last bit reduces the image size from over a gigabyte to about 20 megabytes
FROM scratch

WORKDIR /app

COPY --from=0 /frontend/public ./frontendV2/public

COPY --from=1 /backend/funholidaysapi ./

COPY --from=1 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

COPY doc.md .env ./

ENV PORT 5000

CMD [ "./funholidaysapi" ]