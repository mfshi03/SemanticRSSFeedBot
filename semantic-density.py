import nltk
import openai
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download the required resources
openai.api_key = os.environ.get("OPENAI")

def semantic_density(text):
    # Tokenize the text
    words = word_tokenize(text)

    # Tag the words with their part of speech
    pos_tags = nltk.pos_tag(words)

    # Define the content word tags
    content_word_tags = ['NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']

    # Count the content words
    print(pos_tags)
    content_words_count = sum(1 for word, tag in pos_tags if tag in content_word_tags)

    # Calculate the semantic density
    density = content_words_count / len(words)

    return density

text = '''
large-language models simulate actual environments using text as context
'''

completion = openai.ChatCompletion.create(
    model="gpt-4", 
    messages=[
        {"role": "system", "content":'''
        Audience: 
        Translate this text to make it more rare and complex.
        '''},
        {"role": "user", "content": text},
        ]
    )

print("New: " + completion["choices"][0]["message"]["content"])
new_text = completion["choices"][0]["message"]["content"]
completion = openai.ChatCompletion.create(
    model="gpt-4", 
    messages=[
        {"role": "system", "content":'''
        Audience: 
        Rate how generic and complex text is based on a decimal from 0-1 where 1 is the most rare and complex possible text.
        '''},
        {"role": "user", "content": text},
        ]
    )
print("Value: " + completion["choices"][0]["message"]["content"])



density = semantic_density(text)
print(f"Semantic density: {density:.2f}")