import unittest
from metrics import get_keywords_from_data_list

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

if __name__ == '__main__':
    unittest.main()