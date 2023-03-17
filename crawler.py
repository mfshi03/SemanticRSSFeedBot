import json
import os
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup

DIFFBOT = os.environ.get("DIFFBOT_TOKEN")


def scrape_request(url:str) -> str:
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.text

def find_values(id:str, json_repr:str) -> str:
    '''
    Finds relevant info from JSON text
    '''
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict) # Return value ignored.
    return results
  
def crawl(url:str) -> str:
    '''
    This returns a string of all important text on a webpage
    '''
    crawl_url = url 
    query_url = crawl_url = urllib.parse.quote(crawl_url)
    request_url = "https://api.diffbot.com/v3/article?token=" + DIFFBOT +  "&url=" + query_url
    headers = {"accept": "application/json"}

    response = requests.get(request_url, headers=headers)
    text = "No text"

    if response.status_code == 200:
        if "errorCode" in response.text:
            request_url = "https://api.diffbot.com/v3/discussion?token=" + DIFFBOT +  "&url=" + crawl_url
            headers = {"accept": "application/json"}
            response = requests.get(request_url, headers=headers)
        if "errorCode" in response.text:
            request_url = "https://api.diffbot.com/v3/analyze?token=" + DIFFBOT +  "&url=" + crawl_url 
            headers = {"accept": "application/json"}
            response = requests.get(request_url, headers=headers)
        data = response.text
        title = []
        text = ""
        latent_text = " ".join(find_values('text', data))
        summary = " ".join(find_values('summary',data))
        title =  " ".join(find_values('title', data))
        
    
    text += "Title:" + title + "\n\n" if len(title) > 3 else ""
    #text += "Summary:" + summary + "\n\n" if len(summary) > 3 else ""
    text += "Text:" + latent_text if len(latent_text) > 3 else ""

    text = re.sub(' +', ' ', text)
    return text[0:900]