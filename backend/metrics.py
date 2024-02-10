import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import re
from textblob import TextBlob
from stop_words import get_stop_words
import take

def get_metrics(posts):
    for post in posts:
        post['sentiment_rate'] = 1

    return {
        'total_positives': 5,
        'total_negatives': 1,
        'total_neutral': 2,
        'posts': posts,
        'keywords': [
            {
                'word': 'tezza',
                'value': 0.01986307225913374
            },
            {
                'word': 'кордон',
                'value': 0.024781376509218734
            },
            {
                'word': 'подружжя',
                'value': 0.02570533806449336
            }
        ]
    }


def merge_metrics(results):
    posts = []
    for result in results:
        posts.extend(result['posts'])
    return {
        'total_positives': 5,
        'total_negatives': 1,
        'total_neutral': 2,
        'posts': posts,
        'keywords': [
            {
                'word': 'tezza',
                'value': 0.01986307225913374
            },
            {
                'word': 'кордон',
                'value': 0.024781376509218734
            },
            {
                'word': 'подружжя',
                'value': 0.02570533806449336
            }
        ]
    }

def get_keywords(post):
  stop_words_ukr = get_stop_words('ukrainian')
  stop_words_eng = get_stop_words('english')
  stopwords_specific = stop_words_eng + stop_words_ukr

  language = "eng"
  max_ngram_size = 1
  deduplication_threshold = 0.5
  deduplication_algo = 'seqm'
  windowSize = 3
  numOfKeywords = 10

  kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None, stopwords=stopwords_specific)
  return kw_extractor.extract_keywords(post)

def get_keywords_from_data_list(data_list):
    all_content = ""
    for data in data_list:
        content = data["content"]
        all_content += content + " "
    keywords = get_keywords(all_content)
    keywords_data = {
        "keywords": keywords,
    }
    return keywords_data


def sentiment_analyser(data_list):
    sentiment_objects = [TextBlob(data["content"]) for data in data_list]
    sentiment_values = [[data.sentiment.polarity, str(data)] for data in sentiment_objects]
    sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "content"])

    total_positives = sum(1 for i in sentiment_df["polarity"] if i > 0)
    total_negatives = sum(1 for i in sentiment_df["polarity"] if i < 0)
    total_neutral = sum(1 for i in sentiment_df["polarity"] if i == 0)

    posts_data = []

    for index, row in sentiment_df.iterrows():
        post_info = {
            "sentiment_rate": row["polarity"],
            "content": row["content"],
            "created": data_list[index]["timestamp"],
            # тайтл (тільки для новин) і соурс
        }
        posts_data.append(post_info)

    result = {
        "total_positives": total_positives,
        "total_negatives": total_negatives,
        "total_neutral": total_neutral,
        "posts": posts_data,
     }

    return result


def combined_function(data_list):
    sentiment_result = sentiment_analyser(data_list)
    keywords_result = get_keywords_from_data_list(data_list)

    sentiment_result["keywords"] = keywords_result["keywords"]
    return sentiment_result

