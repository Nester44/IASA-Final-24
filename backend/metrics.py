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
