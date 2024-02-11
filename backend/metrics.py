import pandas as pd
from textblob import TextBlob
from stop_words import get_stop_words
import yake
import string

def get_keywords(post):
  stop_words_ukr = get_stop_words('ukrainian')
  stop_words_eng = get_stop_words('english')
  stopwords_specific = stop_words_eng + stop_words_ukr

  language = "eng"
  max_ngram_size = 1
  deduplication_threshold = 0.5
  deduplication_algo = 'seqm'
  windowSize = 3
  numOfKeywords = 20

  kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None, stopwords=stopwords_specific)
  return kw_extractor.extract_keywords(post)

def preprocess(content):
    to_delete = string.punctuation + '-«»“’'
    result = content.translate(str.maketrans('', '', to_delete))
    return result.lower()

def get_keywords_from_data_list(data_list):
    all_content = ""
    for data in data_list:
        content = preprocess(data["content"])
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
        data_list[index]["sentiment_rate"] = row["polarity"]
        data_list[index]["content"] = data_list[index]["content"][:255]
        posts_data.append(data_list[index])

    result = {
        "total_positives": total_positives,
        "total_negatives": total_negatives,
        "total_neutral": total_neutral,
        "posts": posts_data,
     }

    return result


def get_metrics(data_list):
    sentiment_result = sentiment_analyser(data_list)
    keywords_result = get_keywords_from_data_list(data_list)

    sentiment_result["keywords"] = keywords_result["keywords"]
    return sentiment_result

