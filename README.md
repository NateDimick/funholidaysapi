# Fun Holidays

Over 7000 Holidays that you may or may not have heard of that happen annually - all conveniently available through this API.

Ever wondered what obscure holidays were today? On your birthday? Or this month? Or how many pizza-related holidays there are?

This might be the most complete list of Holidays on the internet - I've aggregated from many sources so all your queries produce the most complete and accurate results!

## Functions

All API urls are extended off of /api

### GET /today

arguements: none

returns all of the holidays that take place on the date of the GET request in GMT +/- 0:00

```JSON
GET /api/today

{
    "day": 27,
    "month": 8,
    "holidays": ["Banana Lovers Day", "The Duchess Who Wasnt Day", "The Duchess Who Wasn't Day", "Petroleum Day", "Tug-of-War Day", "International Bat Night", "National Pots de Cr\u00e8me Day", "Burger Day", "Pots De Creme Day", "National Banana Lovers Day", "International Lottery Day"]
}
```

### GET /date

arguments: month, day (both required, both ints.)

returns all annual holidays that take place on month/day/year

``` JSON

GET /api/date?month=11&day=26

{
    "day": 26,
    "month": 11,
    "holidays": ["A Blue Christmas", "National Cake Day", "Cakes Day", "Turkey Free Thanksgiving", "Cake Day", "Day of Mourning"]
}

```

### GET /random

arguements: none

returns the date and name of a single random holiday on that date

``` JSON
GET /api/random

{
    "month": 1,
    "day": 31,
    "holiday": "Gorilla Suit Day"
}
```

### GET /month

arguments: month (int, required)

returns all the holidays that take place in the specified month, grouped by the day they occur on.

``` JSON
GET /api/month?month=4

{
    "month": 4,
    "holidays": {
        "1": ["Reading Is Funny Day", "Fun at Work Day", "Day Of Hope", "One Cent Day", "Sourdough Bread Day", "Fun Day"],
        "2": ["Love Your Produce Manager Day", "Ferret Day", "National Peanut Butter and Jelly Day", "Peanut Butter and Jelly Day", "World Autism Day", "Children's Book Day", "Tell A Lie Day"],
        "3": ["National Find a Rainbow Day", "World Party Day", "Poet in a Cupcake Day", "Tweed Day", "Fish Fingers and Custard Day", "Find A Rainbow Day", "Chocolate Mousse Day", "Walk to Work Day"],
        "4": ...
```

### GET /when

arguements: like (string, required, unless you want the entire contents of the database returned)

returns all the holidays that have titles that pattern match the like argument, sorted by date

``` JSON
GET /api/when?like=pizza

{
    "2": {
        "9": ["Pizza Day", "National Pizza Day (at least five slices)[1]"],
        "10": ["Great American Pizza Bake"],
        "16": ["Great American Pizza Bake"]
        },
    "4": {
        "5": ["Deep Dish Pizza Day"]
        },
    "5": {
        "15": ["Pizza Party Day"]
        },
    "9": {
        "5": ["National Cheese Pizza Day", "Cheese Pizza Day"],
        "20": ["Pepperoni Pizza Day", "National Pepperoni Pizza Day"]
        },
    "10": {
        "9": ["Beer and Pizza Day", "International Beer and Pizza Day"],
        "11": ["Sausage Pizza Day", "National Sausage Pizza Day"]
        },
    "11": {
        "12": ["Pizza With The Works Except Anchovies Day", "National Pizza with the Works Except Anchovies Day"]
        }
}

```

## About the Data

The data for this app has been scraped from:

* [timeanddate.com](https://www.timeanddate.com/holidays/fun/)
* [nationaltoday.com](https://nationaltoday.com/fun-holidays/)
* [blankcalendarpages.com](https://blankcalendarpages.com/holidays/fun)
* [wikipedia.org](https://en.wikipedia.org/wiki/List_of_food_days)
* [wikipedia.org again](https://en.wikipedia.org/wiki/List_of_minor_secular_observances)
* [daysoftheyear.com](https://www.daysoftheyear.com/)
* [anydayguide.com](https://anydayguide.com/calendar/)
* [checkiday.com](https://checkiday.com)

Can't find a holiday that you expect?

* suggest adding it under the issues for this project on github
* create a pr and add it yourself
  * prefereably, follow the procedure in the holiday_agg directory
