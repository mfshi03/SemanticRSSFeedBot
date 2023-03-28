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

hrefs = [a["href"] for a in references if "https" in a['href'] and "url" in a['href']]
search_urls = []
for href in hrefs:
    match = re.search(r'/url\?q=(.*?)&sa',href)
    if match:
        search_urls.append(match.group(1))

print(search_urls)
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
        {"role": "user", "content": f"Summarize this information: {information}\nUse the information/summary to relate to a multi-step solution to this query: {query}"},
    ]
)


print("Summary: " + completion["choices"][0]["message"]["content"])
