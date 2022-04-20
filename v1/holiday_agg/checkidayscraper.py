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
    for day_num in range(month_days[month_num]):
        day = str(day_num + 1)

        url = f"https://www.checkiday.com/{m}/{day}/2020"  # url to scrape from daysoftheyear.com
        print(month, url)
        # disguise user agent to prevetn 403 forbidden
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})  # https://medium.com/@raiyanquaium/how-to-web-scrape-using-beautiful-soup-in-python-without-running-into-http-error-403-554875e5abed
        source = urlopen(req).read()
        soup = BeautifulSoup(source)
        events = soup.findAll("h2", {"class": "mdl-card__title-text"})
        print(len(events), " possible holidays found")
        for e in events:
            try:
                date = e.find_all("span")[0].decode_contents()
                date = ' '.join(date.split()[:2])  # keep just the first two words
                if month and day in date:
                    holiday = e.find_all("a")[0].decode_contents()
                    rows.append((int(m), int(day), holiday))
            except:
                pass

        sleep(5)

with open("fun_holidays_7.txt", 'a', encoding="UTF-8") as file:
    for row in rows:
        r = '\t'.join([str(x) for x in row])
        file.write(f"{r}\n")