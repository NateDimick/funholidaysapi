"""
this actually exports a tsv, sooooo...
"""
import csv, html
from textdistance import levenshtein
from re import search

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

def main():
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
        # data scraped from https://www.daysoftheyear.com/days/2020/{month}/{day}/ with daysoftheyearscraper.py
        with open("fun_holidays_4.txt", "r", encoding="UTF-8") as f:
            for line in f:
                month, day, holiday = html.unescape(line).replace('\uFFFD', "'").split('\t')
                if "Month" not in holiday and "Week" not in holiday:
                    rows.append((int(month), int(day), holiday.strip()))
        # data scraped from https://anydayguide.com/calendar/{day}-{month}-2020 with anydayguidescraper.py
        with open("fun_holidays_5.txt", "r", encoding="UTF-8") as f:
            for line in f:
                month, day, holiday = html.unescape(line).replace('\uFFFD', "'").split('\t')
                if "Month" not in holiday and "Week" not in holiday:
                    rows.append((int(month), int(day), holiday.strip()))
        # copied from https://en.wikipedia.org/wiki/List_of_minor_secular_observances
        with open("fun_holidays_6.txt", "r", encoding="UTF-8") as f:
            for line in f:
                cols = line.split('\t')
                if len(cols) > 1 and line[:3] in months.keys():
                    try:
                        month = months[cols[0][:3]]
                        day = int(cols[0].split()[1].split("(")[0][:2])
                        holiday = cols[1].split("[")[0]
                        rows.append((month, day, holiday))
                    except:
                        print(line)
        # data scraped from https://checkiday.com/{month}/{day}/2020
        with open("fun_holidays_7.txt", "r", encoding="UTF-8") as f:
            for line in f:
                month, day, holiday = html.unescape(line).replace('\uFFFD', "'").split('\t')
                if "Month" not in holiday and "Week" not in holiday:
                    rows.append((int(month), int(day), holiday.strip()))
        # the fakest hlidays - ones made up that are exclusive to this dataset, just to see if any future data sets carry these then that means this db was the source
        with open("copy_trap.txt", "r") as f:
            for line in f:
                month, day, holiday = line.split(",")
                rows.append((int(month), int(day), holiday.strip()))

        rowset = set(rows)
        rows = list(rowset)
        rows.sort(key=lambda x: (x[0], x[1]))
        rows = remove_near_duplicates(rows)
        rows = remove_multiday_duplicates(rows)
        print(len(rows), len(set([h[2] for h in rows])))
        writer.writerows(rows)

def remove_near_duplicates(rowlist):
    """
    check holidays against each other that are on the same date
    see if they are similar - check the intersection of the sets of thw words that compose them
    if only one mismatch - caused by "national" or an apostrophe, keep the longer one, ditch the shorter one
    """
    def inner_duplicates(hList):
        set_list = {h: set(h.lower().split()) for h in hList}  # map of holidays to their word sets
        new_list = []  # output set
        banned = set()
        for i, h1 in enumerate(hList):
            if h1 not in banned:
                s1 = set_list[h1]
                matches = []
                for h2 in hList[i+1:]:
                    s2 = set_list[h2]
                    intersection = s1.intersection(s2)
                    difference = s1.symmetric_difference(s2)
                    if len(intersection) > 1 and 1 <= len(difference) <= 2:  # accounts for single differences (National added or not) and spelling differences (apostorphe)
                        if len(difference) > 1:
                            # checking edit distance chnged dataset from 5366 entries to 5588 entries
                            if levenshtein(h1.lower(), h2.lower()) < 3:  # only a match if the two strings are very similar
                                matches.append(h2)
                            #print(difference, h1, h2)
                        else:
                            matches.append(h2)  # if difference == 1 then it's just an addition/ subtraction of one word, they match
                if matches:
                    matches.append(h1)
                    matches.sort(key=lambda x: len(x), reverse=True)  # sort by longest first
                    new_list.append(matches[0])  # longest title is kept
                    for m in matches:
                        banned.add(m)
                else:
                    new_list.append(h1)  # no matches, h1 is unique, keep it in the list
        return new_list
            

    newList = []
    today = []
    d, m = 0, 0
    for row in rowlist:
        month, day, holiday = row
        if m != month or d != day:
            newList += [(m, d, h) for h in inner_duplicates(today)]
            today = [holiday]
            d, m = day, month
        else:
            today.append(holiday)
    newList += [(m, d, h) for h in inner_duplicates(today)]
    return newList

def remove_multiday_duplicates(rowlist):
    hset = set()
    new_list = []
    for row in rowlist:
        h = row[2]
        if h.lower() not in hset:
            hset.add(h.lower())
            new_list.append(row)

    return new_list


main()
