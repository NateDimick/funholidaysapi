from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from time import sleep
from html import unescape

month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # dict seems like too much here
months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
m_codes = {months[k]: k for k in months.keys()}
rows = []

for month_num in range(12):
    month = m_codes[month_num + 1]  # three letter code to check against web page
    m = str(month_num + 1)
    print(month)
    if len(m) == 1:
        m = "0" + m
    for day_num in range(month_days[month_num]):
        day = str(day_num + 1)
        if len(day) == 1:
            day = "0" + day
    
        url = f"https://anydayguide.com/calendar/{day}-{m}-2020"  # url to scrape from anydayguide.com
        print(url)
        # disguise user agent to prevetn 403 forbidden
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})  # https://medium.com/@raiyanquaium/how-to-web-scrape-using-beautiful-soup-in-python-without-running-into-http-error-403-554875e5abed
        source = urlopen(req).read()
        soup = BeautifulSoup(source)
        days = soup.findAll("h3", {"class": "title"})  # find all the cards on the page
        print(len(days), " : number of events found")
        for d in days:
            a = d.find_all("a")[0]
            rows.append((int(m), int(day), unescape(a['title'])))
        
        sleep(5)  # 5 second interval = 1/2 hour to scrape all data

with open("fun_holidays_5.txt", 'a') as file:
    for row in rows:
        r = '\t'.join([str(x) for x in row])
        file.write(f"{r}\n")