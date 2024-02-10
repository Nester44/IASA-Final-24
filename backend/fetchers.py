from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import datetime, timedelta

import os

import requests
from bs4 import BeautifulSoup
import html2text
import locale
import json


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
    try:
        time_element = tweet.find_element(By.TAG_NAME, 'time')
        time_text = time_element.get_attribute('datetime')
        time_obj = datetime.strptime(time_text, "%Y-%m-%dT%H:%M:%S.%fZ")
        return int(time.mktime(time_obj.timetuple()))
    except NoSuchElementException:
        return ''


def _get_tweet_username(tweet):
    try:
        name_element = tweet.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
        for spans in name_element.find_elements(By.TAG_NAME, 'span'):
            if '@' in spans.text:
                return spans.text
    except NoSuchElementException:
        return ''


class Fetcher:
    def __init__(self):
        self.days = 1
        self.min_timestamp = datetime.timestamp(datetime.today() - timedelta(days=1))

    def set_period(self, days):
        self.days = days
        self.min_timestamp = datetime.timestamp(datetime.today() - timedelta(days=days))


class XFetcher(Fetcher):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://x.com'
        self.search_params = '/search?q={}&src=typed_query&f=top'
        self.base_scrolls = 5
        self.scroll_increase = 0.75

        self.driver = webdriver.Firefox()
        self.driver.get(self.base_url)
        self.driver.add_cookie({"name": "auth_token", "value": os.environ.get('TWITTER_COOKIE')})

    def __parse(self, tweet):
        post = {'created': _get_tweet_timestamp(tweet)}
        if post['created'] < self.min_timestamp:
            return None

        try:
            text = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            post['content'] = text.text
        except NoSuchElementException:
            post['content'] = ''

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

        scrolls = self.base_scrolls + (self.days - 1) * self.scroll_increase

        posts = []
        for _ in range(int(scrolls)):
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

            post['created'] = _get_mctoday_timestamp(soup)
            if post['created'] < self.min_timestamp:
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


def scrape_content_bbc(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            rich_text_wrappers = soup.find_all(class_="ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0")
            article_content = ''.join([wrapper.get_text() for wrapper in rich_text_wrappers])
            return article_content
        else:
            print('Request error:', response.status_code)
    except Exception as e:
        print('Error occurred while parsing the page:', e)


def scrape_content_cnn(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            rich_text_wrappers = soup.find_all(class_="paragraph inline-placeholder")
            article_content = ''.join([wrapper.get_text() for wrapper in rich_text_wrappers])
            return article_content
        else:
            print('Request error:', response.status_code)
    except Exception as e:
        print('Error occurred while parsing the page:', e)


def scrape_content_breitbart(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            rich_text_wrappers = soup.find_all(class_="entry-content")
            article_content = ''.join([wrapper.get_text() for wrapper in rich_text_wrappers])
            return article_content
        else:
            print('Request error:', response.status_code)
    except Exception as e:
        print('Error occurred while parsing the page:', e)


def create_article_dict(article):
    source_to_function = {
        'bbc-news': scrape_content_bbc,
        'cnn': scrape_content_cnn,
        'breitbart-news': scrape_content_breitbart
    }

    scrape_function = source_to_function.get(article['source']['id'])
    content = scrape_function(article['url'])

    return {
        "source": article["source"],
        "title": article["title"],
        "url": article["url"],
        "created": article["publishedAt"],
        "content": content
    }


def get_articles_from_sources(search_query, api_key, sources, from_date, to_date):
    params = {'q': search_query, 'apiKey': api_key, 'sources': ','.join(sources), 'from': from_date, 'to': to_date}
    url = 'https://newsapi.org/v2/everything'

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            concrete_data_list = []
            if "articles" in data:
                for article in data["articles"]:
                    concrete_data_list.append(create_article_dict(article))
                print(json.dumps(concrete_data_list, indent=4))

            return concrete_data_list
        else:
            print('Request error:', response.status_code)
    except Exception as e:
        print('Error occurred:', e)


class NewsFetcher(Fetcher):
    def fetch_all(self, query, url_scraper, sources):

        # From_date depends on the mode selected by the user
        from_date = datetime.timestamp(datetime.today() - timedelta(days=1))

        api_key = os.environ.get('NEWS_API_KEY')

        # Search_query is set by input
        search_query = ''

        return get_articles_from_sources(search_query, api_key, sources, from_date, self.min_timestamp)

