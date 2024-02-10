from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from fetchers import XFetcher, MctodayFetcher, period_to_days
from metrics import get_metrics, merge_metrics

app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["GET"])
@cross_origin()
def hello_world():
    return jsonify({"message": "Hello, World!"})


source_fetchers = {
    'twitter': XFetcher(),
    'mctoday': MctodayFetcher()
}


@app.route("/analytics", methods=["GET"])
@cross_origin()
def fetch():
    query = request.args.get('q')
    if query is None:
        return "Query aren't specified", 400
    sources = request.args.get('sources')
    if sources is None:
        return "Sources aren't specified", 400
    period = request.args.get('period')
    days = period_to_days(period)
    if days is None:
        return "Invalid time period", 400

    fetchers = []
    for source in sources.split(','):
        if source not in source_fetchers:
            return "Unknown source", 400
        fetcher = source_fetchers[source]
        fetchers.append(fetcher)

    results = []
    post_id = 0
    for fetcher in fetchers:
        fetcher.set_period(days)
        posts = fetcher.fetch(query)
        for post in posts:
            post['id'] = post_id
            post_id += 1
        results.append(get_metrics(posts))

    return jsonify(merge_metrics(results))


if __name__ == "__main__":
    app.run(debug=True)
