from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from fetchers import XFetcher

app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["GET"])
@cross_origin()
def hello_world():
    return jsonify({"message": "Hello, World!"})


fetchers = {
    'x': XFetcher
}


@app.route("/fetch", methods=["GET"])
@cross_origin()
def fetch():
    query = request.args.get('q')
    if query is None:
        return "Query aren't specified", 400
    sources = request.args.get('sources')
    if sources is None:
        return "Sources aren't specified", 400
    # Does not work yet
    period = request.args.get('period')

    # Only X works for now
    if sources == 'x':
        fetcher = fetchers[sources]()
        posts = fetcher.fetch(query)
        for post in posts:
            post['source'] = sources
            post['sentiment_rate'] = 1

        return jsonify({
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
        })
    else:
        return "Not supported yet", 418

    # for source in sources:


if __name__ == "__main__":
    app.run(debug=True)
