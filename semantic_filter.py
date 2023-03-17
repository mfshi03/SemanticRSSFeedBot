import os
import json 
import pickle
import openai
import numpy as np
import pandas as pd
from typing import List
from scipy import spatial

openai.api_key = os.environ.get("OPENAI")
embedding_cache_path = "embeddings_cache.pkl"
# load the cache if it exists, and save a copy to disk

embedding_cache = pd.read_pickle(embedding_cache_path)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def distances_from_embeddings(
    query_embedding: List[float],
    embedding: List[float],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }

    return distance_metrics[distance_metric](query_embedding, embedding)


# define a function to retrieve embeddings from the cache if present, and otherwise request via the API
def embedding_from_string(
    string: str,
    model: str="text-embedding-ada-002",
    embedding_cache=embedding_cache
) -> list:
    """Return embedding of given string, using a cache to avoid recomputing."""
    if (string, model) not in embedding_cache.keys():
        embedding_cache[(string, model)] = openai.Embedding.create(input=string, model="text-embedding-ada-002")["data"][0]["embedding"]
        with open(embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(embedding_cache, embedding_cache_file)
    return embedding_cache[(string, model)]

def listwise_ranking(query: str) -> dict:
    '''
    Returns the dict of the listwise ranking 
    '''
    query_embedding = embedding_from_string(query)
    article_embeddings = {}

    with open("cache.json", "r") as f:
        cache = json.load(f)

    for blog in cache:
        if blog == "time" or blog == "py":
            continue
        for article in cache[blog]:
            embedding = embedding_from_string(article['title'])
            e1 = embedding
            e2 = query_embedding
            total = distances_from_embeddings(e1, e2)
            #print(article["title"], total)
            #print(e1, e2)
            if "button" not in article:
                article_embeddings[(article['title'],article['link'])] = total
            else:
                article_embeddings[(article['title'],article['button'])] = total

    titles = []
    links = []
    similarity = []
    for k, v in sorted(article_embeddings.items(), key=lambda x: x[1]):
        titles.append(k[0])
        links.append(k[1])
        similarity.append(v)
    
    return [titles, links, similarity]

def rank_urls(query:str, results:str) -> str:
    article_embeddings = {}
    query_embedding = embedding_from_string(query)
    for result in results:
        embedding = embedding_from_string(result)
        dist = distances_from_embeddings(query_embedding, embedding)
        article_embeddings[result] = dist
        
    titles = [k for k, v in sorted(article_embeddings.items(), key=lambda x: x[1])]
    return titles





if __name__ == "__main__":
    with open("cache.json", "r") as f:
        cache = json.load(f)
    titles = []
    liked = []

    liked_embeddings = []
    for title in liked:
        embedding = embedding_from_string(title)
        liked_embeddings.append(embedding)


    print("Type in a query:")
    query_embedding = embedding_from_string(input())


    article_embeddings = {}
    for blog in cache:
        if blog == "time" or blog == "py":
            continue
        for article in cache[blog]:
            titles.append(article['title'])
            embedding = embedding_from_string(article['title'])
            e1 = embedding
            e2 = query_embedding
            total = distances_from_embeddings(e1, e2)
            #print(article["title"], total)
            #print(e1, e2)
            if "button" not in article:
                article_embeddings[(article['title'],article['link'])] = total
            else:
                article_embeddings[(article['title'],article['button'])] = total


    for k, v in sorted(article_embeddings.items(), key=lambda x: x[1]):
        print("Title:", k[0])
        print("Link:", k[1])
        print()