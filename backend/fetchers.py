from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from datetime import datetime, timedelta

import os

_time_periods = {
    'day': 1,
    'week': 7,
    'month': 30
}


def period_to_days(period):
    if period is None:
        return _time_periods['day']
    return _time_periods.get(period)


_base_url = 'https://x.com'
_search_params = '/search?q={}&src=typed_query&f=top'


def _get_timestamp(tweet):
    time_element = tweet.find_element(By.TAG_NAME, 'time')
    time_text = time_element.get_attribute('datetime')
    time_obj = datetime.strptime(time_text, "%Y-%m-%dT%H:%M:%S.%fZ")
    return time.mktime(time_obj.timetuple())


class XFetcher:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.min_timestamp = datetime.timestamp(datetime.today() - timedelta(days=1))

    def set_period(self, days):
        self.min_timestamp = datetime.timestamp(datetime.today() - timedelta(days=days))

    def __parse(self, tweet):
        post = {'created': _get_timestamp(tweet)}
        if post['created'] < self.min_timestamp:
            return None

        text = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
        post['content'] = text.text

        post['source'] = {
            'id': 'twitter',
            'name': 'Twitter'
        }

        return post

    def fetch(self, query):
        self.driver.get(_base_url)
        self.driver.add_cookie({"name": "auth_token", "value": os.environ.get('TWITTER_COOKIE')})
        self.driver.get(_base_url + _search_params.format(query))
        # Wait for the first batch of data
        time.sleep(1)

        posts = []
        for _ in range(5):
            tweets = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            for tweet in tweets:
                article = self.__parse(tweet)
                if article is not None:
                    posts.append(article)

            # Scroll down to load more data
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait instead for loader to disappear
            time.sleep(0.5)

        return posts
