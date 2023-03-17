import os
import openai
import requests
import urllib.parse
import json
import re
from bs4 import BeautifulSoup
from crawler import crawl
from semantic_filter import rank_urls

with open("DIFFBOT.json", "r") as f:
    cache = json.loads(f.read())

DIFFBOT_TOKEN = os.environ.get("DIFFBOT_TOKEN")
openai.api_key = os.environ.get("OPENAI")

print("Type in your query:")
query = str(input())
qstring = query.strip().replace(" ", "+")
url =  f"https://google.com/search?q={qstring}"

request_url = "https://api.diffbot.com/v3/list?token=" + DIFFBOT_TOKEN +  "&url=" + url
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
references = soup.findAll('a')

search_urls = [re.search(r'/url\?q=(.*?)&sa', a["href"]).group(1) for a in references if "https" in a['href'] and "url" in a['href']]
results = rank_urls(query, search_urls)
information = ""
for result in results[0:3]:
    link = result
    print("Link:",link)
    text = ""
    if link not in cache:
        text = crawl(url=link)
        with open("DIFFBOT.json", "w") as f:
            json.dump(cache, f)
    else: 
        text = cache[link]
    information += text + "\n"

print(information)
search_results = []
completion = openai.ChatCompletion.create(
model="gpt-3.5-turbo", 
messages=[
    {
        "role": "system", "content": f"Use the information: [{information}] to answer any queries with around 200 words"
    },
        {"role": "user", "content": f"Think about this information: {information}"},
    ]
)


print("Summary: " + completion["choices"][0]["message"]["content"])


