from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from fetchers import XFetcher, MctodayFetcher, NewsFetcher, period_to_days, generate_rss_feed
from metrics import get_metrics

import concurrent.futures

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

news_fetchers = ['bbc-news', 'cnn', 'breitbart-news']

@app.route("/analytics", methods=["GET"])
@cross_origin()
def analytics():
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

    def fetch_from(f):
        f.set_period(days)
        posts = []
        if isinstance(f, NewsFetcher):
            if len(news_sources) != 0:
                posts.extend(f.fetch_all(query, news_sources))
        else:
            posts.extend(f.fetch(query))
        return posts

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_from, fetchers + [nf]))

    post_list = []
    for result in results:
        post_list.extend(result)

    return get_metrics(post_list)

@app.route("/rss", methods=["GET"])
@cross_origin()
def rss():
    query = request.args.get("q")
    if query is None:
        return "Query aren't specified", 400
    return generate_rss_feed(query, news_fetchers)

if __name__ == "__main__":
    app.run(debug=True)
