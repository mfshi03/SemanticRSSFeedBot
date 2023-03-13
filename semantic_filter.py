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
try:
    embedding_cache = pd.read_pickle(embedding_cache_path)
except FileNotFoundError:
    embedding_cache = {}
with open(embedding_cache_path, "wb") as embedding_cache_file:
    pickle.dump(embedding_cache, embedding_cache_file)

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

with open("cache.json", "r") as f:
    cache = json.load(f)
titles = []
liked = ["prestigious us school","How Facebook/Meta Design Sustainable Datacenters with AI - Bilge Acun | Stanford MLSys #52", "super-smart", "Training an Object Detection model in RunwayML to Analyze Posters"]

liked_embeddings = []
for title in liked:
    embedding = embedding_from_string(title)
    liked_embeddings.append(embedding)

article_embeddings = {}
for blog in cache:
    if blog == "time" or blog == "py":
        continue
    for article in cache[blog]:
        titles.append(article['title'])
        embedding = embedding_from_string(article['title'])
        e1 = embedding
        e2 = liked_embeddings[0]
        total = distances_from_embeddings(e1, e2)
        #print(article["title"], total)
        #print(e1, e2)
        article_embeddings[(article['title'],article['link'])] = total


for k, v in sorted(article_embeddings.items(), key=lambda x: x[1]):
    print("Title:", k[0])
    print("Link:", k[1])
    print()