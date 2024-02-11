from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from fetchers import XFetcher, MctodayFetcher, NewsFetcher, period_to_days
from metrics import get_metrics

app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["GET"])
@cross_origin()
def hello_world():
    return jsonify({"message": "Hello, World!"})

# ids are: mctoday, bbc, cnn, twitter, breitbart
source_fetchers = {
    'twitter': XFetcher(),
    'mctoday': MctodayFetcher()
}

nf = NewsFetcher()

news_fetchers = {'bbc': 'bbc-news', 'cnn': 'cnn', 'breitbart': 'breitbart-news'}

@app.route("/analytics", methods=["GET"])
@cross_origin()
def fetch():
    query = request.args.get("q")
    if query is None:
        return "Query aren't specified", 400
    sources = request.args.get("sources")
    if sources is None:
        return "Sources aren't specified", 400
    period = request.args.get('period')
    days = period_to_days(period)
    if days is None:
        return "Invalid time period", 400

    fetchers = []
    news_sources = []
    for source in sources.split(','):
        if source in source_fetchers:
            fetcher = source_fetchers[source]
            fetchers.append(fetcher)
        elif source in news_fetchers:
            news_sources.append(source)
        else:
            return "Unknown source", 400

    results = []
    post_id = 0
    for fetcher in fetchers:
        fetcher.set_period(days)
        posts = fetcher.fetch(query)
        for post in posts:
            post['id'] = post_id
            post_id += 1
        results.extend(posts)
    
    if len(news_sources) != 0:
        nf.set_period(days)
        news_sources_keys = [news_fetchers[source] for source in news_sources]
        posts = nf.fetch_all(query, news_sources_keys)
        for post in posts:
            post['id'] = post_id
            post_id += 1
        results.extend(posts)

    return get_metrics(results)


if __name__ == "__main__":
    app.run(debug=True)
