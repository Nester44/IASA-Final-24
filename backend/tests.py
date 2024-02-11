import unittest
from metrics import get_keywords_from_data_list, get_metrics
from mock import patch
from fetchers import period_to_days

class TestMetricsMethods(unittest.TestCase):
    def test_keywords_obvious(self):
        data = [
            {
                "content": "Cherries are tasty"
            },
            {
                "content": "Have you never tasted cherries?"
            },
            {
                "content": "There are some cherries on the table"
            },
            {
                "content": "The, the, the, the"
            }
        ]

        keywords = get_keywords_from_data_list(data)['keywords']

        self.assertEqual(keywords[0][0], 'cherries')

    def test_keywords_no_stopwords(self):
        data = [
            {
                "content": "Are difficult, are complex"
            },
            {
                "content": "No, no, please"
            },
            {
                "content": "The most, the least"
            },
        ]
        stopwords = ['are', 'no', 'the']

        keywords = get_keywords_from_data_list(data)['keywords']

        for [k, _] in keywords:
            self.assertNotIn(k, stopwords)

    @patch('metrics.get_keywords_from_data_list', return_value={'keywords': 'test'})
    @patch('metrics.sentiment_analyser', return_value={})
    def test_metrics_combination(self, mock_keywords, mock_sentiment):
        metrics = get_metrics([])
        self.assertEqual(metrics['keywords'], 'test')

class TestFetcherMethods(unittest.TestCase):
    def test_period_conversion_day(self):
        days = period_to_days('day')
        self.assertEqual(days, 1)

    def test_period_conversion_week(self):
        days = period_to_days('week')
        self.assertEqual(days, 7)

    def test_period_conversion_month(self):
        days = period_to_days('month')
        self.assertEqual(days, 30)

    def test_period_conversion_empty(self):
        days = period_to_days(None)
        self.assertEqual(days, 1)


if __name__ == '__main__':
    unittest.main()