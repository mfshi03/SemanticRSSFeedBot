import os 
import json
import semantic_filter as fil

with open("cache.json", "r") as f:
    cache = json.loads(f.read())

selection = []
for blog in cache:
    if blog == "time" or blog == "py":
            continue
    for article in cache[blog]:
        if "button" not in article:
            print(article["title"], article["link"])
            selection.append({"title": article["title"], "link": article["link"]})
        else:
            print(article["title"], article["button"])
            selection.append({"title": article["title"], "link": article["button"]})

with open("list.json", "w") as f:
    json.dump(selection, f)