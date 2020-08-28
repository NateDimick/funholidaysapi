"""
this actually exports a tsv, sooooo...
"""
import csv, html

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

with open("fun_holidays.tsv", "w", newline="", encoding="UTF-8") as csv_out:
    writer = csv.writer(csv_out, delimiter="\t")
    rows = []
    # data copied from https://www.timeanddate.com/holidays/fun/
    with open("fun holidays.txt", 'r', encoding="UTF-8") as f:
        for line in f:
            cols = line.strip().split('\t')
            if len(cols) > 1:
                date = cols[0]
                month = months[date.split()[0]]
                day = int(date.split()[1])
                holiday = cols[2]
                rows.append((month, day, holiday))
    # data copied from https://nationaltoday.com/fun-holidays/
    with open("fun_holidays_2.txt", 'r', encoding="UTF-8") as f:
        for i, line in enumerate(f):
            if i % 3 == 0:
                pass
            elif i % 3 == 1:
                day = int(line.split()[1])
                month = months[line.split()[0].lower().capitalize()]
            else:
                holiday = line.split('\t')[0]
                rows.append((month, day, holiday))
    # data copied from https://blankcalendarpages.com/holidays/fun
    with open("fun_holidays_3.txt", 'r', encoding="UTF-8") as f:
        for line in f:
            cols = line.strip().split('\t')
            if len(cols) > 1:
                holiday = cols[0]
                date = cols[1].split(',')[1]
                day = int(date.split()[1])
                month = months[date.strip()[:3]]
                rows.append((month, day, holiday)) 
    # data copied from https://en.wikipedia.org/wiki/List_of_food_days#United_States
    with open("us_food_holidays.txt", "r", encoding="UTF-8") as f:
        for line in f:
            cols = line.split('\t')
            if len(cols) > 1 and line[:3] in months.keys():
                month = months[cols[0][:3]]
                day = int(cols[0].split()[1])
                holiday = cols[1]
                rows.append((month, day, holiday)) 
    # copied from https://en.wikipedia.org/wiki/List_of_food_days#Global
    with open("world_food_days.txt", "r", encoding="UTF-8") as f:
        for line in f:
            cols = line.split('\t')
            if len(cols) > 1 and line[:3] in months.keys():
                month = months[cols[0][:3]]
                day = int(cols[0].split()[1])
                holiday = cols[1]
                rows.append((month, day, holiday))
    # data scraped from https://www.daysoftheyear.com/days/2020/{month}/{day}/ with soupscraper.py
    with open("fun_holidays_4.txt", "r", encoding="UTF-8") as f:
        for line in f:
            month, day, holiday = html.unescape(line).replace('\uFFFD', "'").split('\t')
            if "Month" not in holiday and "Week" not in holiday:
                rows.append((int(month), int(day), holiday.strip()))

    rowset = set(rows)
    rows = list(rowset)
    rows.sort(key=lambda x: (x[0], x[1]))
    rows = [("Month", "Day", "Holiday")] + rows
    writer.writerows(rows)

