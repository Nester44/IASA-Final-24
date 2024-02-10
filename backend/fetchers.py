from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from datetime import datetime, timedelta

import os

import requests
from bs4 import BeautifulSoup
import html2text
import locale


_time_periods = {
    'day': 1,
    'week': 7,
    'month': 30
}


def period_to_days(period):
    if period is None:
        return _time_periods['day']
    return _time_periods.get(period)


def _get_tweet_timestamp(tweet):
    time_element = tweet.find_element(By.TAG_NAME, 'time')
    time_text = time_element.get_attribute('datetime')
    time_obj = datetime.strptime(time_text, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int(time.mktime(time_obj.timetuple()))

def _get_tweet_username(tweet):
    name_element = tweet.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
    for spans in name_element.find_elements(By.TAG_NAME, 'span'):
        if '@' in spans.text:
            return spans.text


class Fetcher:
    def __init__(self):
        self.min_timestamp = datetime.timestamp(datetime.today() - timedelta(days=1))

    def set_period(self, days):
        self.min_timestamp = datetime.timestamp(datetime.today() - timedelta(days=days))


class XFetcher(Fetcher):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://x.com'
        self.search_params = '/search?q={}&src=typed_query&f=top'

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.get(self.base_url)
        self.driver.add_cookie({"name": "auth_token", "value": os.environ.get('TWITTER_COOKIE')})

    def __parse(self, tweet):
        post = {'created': _get_tweet_timestamp(tweet)}
        if post['created'] < self.min_timestamp:
            return None

        text = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
        post['content'] = text.text
        post['author'] = _get_tweet_username(tweet)
        post['url'] = self.base_url + '/{}'.format(post['author'].replace('@', ''))


        post['source'] = {
            'id': 'twitter',
            'name': 'Twitter'
        }

        return post

    def fetch(self, query):
        self.driver.get(self.base_url + self.search_params.format(query))
        # Wait for the first batch of data
        time.sleep(4)

        posts = []
        for _ in range(5):
            tweets = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            for tweet in tweets:
                post = self.__parse(tweet)
                if post is None:
                    continue
                if any(p['author'] == post['author'] and p['created'] == post['created'] for p in posts):
                    continue
                posts.append(post)

            # Scroll down to load more data
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # Wait instead for loader to disappear
            time.sleep(2)

        return posts


def _get_mctoday_content(soup):
    content = ''
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    # Come up with better scraping
    wrapper = soup.select('.content-inner,.post-content,.main-content')[0]
    for paragraph in wrapper.findAll('p'):
        contents = paragraph.contents[0]
        if contents is not None:
            text = h.handle(str(contents))
            content += text

    return content


def _get_mctoday_timestamp(soup):
    date_text = soup.select('.meta-datetime')[0].contents[0]
    locale.setlocale(locale.LC_TIME, 'uk_UA')
    # Set back
    return int(time.mktime(datetime.strptime(str(date_text), "%d %b %Y").timetuple()))


class MctodayFetcher(Fetcher):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://mc.today/uk'

    def fetch(self, query):
        params = {'s': query}
        response = requests.get('https://mc.today/uk', params=params)

        soup = BeautifulSoup(response.content, 'html.parser')
        resources = []
        for title in soup.select('.news-title'):
            title_text = str(title.contents[0])
            resources.append((title_text, title.parent['href']))

        posts = []
        for [title, link] in resources:
            post = {}
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            post['timestamp'] = _get_mctoday_timestamp(soup)
            if post['timestamp'] < self.min_timestamp:
                break

            post['title'] = title
            post['content'] = _get_mctoday_content(soup)
            post['source'] = {
                'id': 'mctoday',
                'name': 'MC.today'
            }
            post['url'] = link

            posts.append(post)

        return posts
