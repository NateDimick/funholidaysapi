"""
This is a scrap file to test code
"""
"""
with open("world_food_days.txt", "r") as f:
    for i, line in enumerate(f):
        print(line.split("\t"))
        if i > 10:
            exit()
"""
err = "Don�t Make Your Bed Day"
import html
print(html.unescape(err))
print(err.encode("UTF-8"))
for c in err:
    print(c, c.encode("UTF-8"))

print(err.replace('\uFFFD', "'"))
print('\uFFFD')

