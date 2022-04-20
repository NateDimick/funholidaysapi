from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from time import sleep
from html import unescape

month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # dict seems like too much here
months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
m_codes = {months[k]: k for k in months.keys()}
rows = []

for month_num in range(11, 12):
    month = m_codes[month_num + 1]  # three letter code to check against web page
    m = str(month_num + 1)
    print(month)
    if len(m) == 1:
        m = "0" + m
    for day_num in range(10, month_days[month_num]):
        day = str(day_num + 1)
        if len(day) == 1:
            day = "0" + day
        

        url = f"https://www.daysoftheyear.com/days/2020/{m}/{day}/"  # url to scrape from daysoftheyear.com
        print(month, url)
        # disguise user agent to prevetn 403 forbidden
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})  # https://medium.com/@raiyanquaium/how-to-web-scrape-using-beautiful-soup-in-python-without-running-into-http-error-403-554875e5abed
        source = urlopen(req).read()
        soup = BeautifulSoup(source)
        # scraping this exact sytle pattern worked on 8/27/2020
        days = soup.findAll("div", {"class": "card__content"})  # find all the cards on the page
        print(len(days), " number of cards found")
        for d in days:
            try:
                subhead = d.find_all("div", {"class": "date_day"})[0].decode_contents()
                event = d.find_all("h3", {"class": "card__title heading"})[0].find_all("a")[0].decode_contents()  # all h3 card__title headings have an a element inside
                if month in subhead and str(int(day)) in subhead:  # events related to other days appear on each day page
                    #print(subhead, event)
                    rows.append((int(m), int(day), unescape(event)))
                else:
                    pass
                    #print("wrong date")
            except:
                pass
        sleep(5)  # sleep for 5 seconds between requests to prevent spamming webserver
        # takes about 30 minutes to scrape a whole year

with open("fun_holidays_4.txt", 'a', encoding="UTF-8") as file:
    for row in rows:
        r = '\t'.join([str(x) for x in row])
        file.write(f"{r}\n")