"""
Article Parser

Module to extract article content using different packages

"""
from bs4 import BeautifulSoup
from newspaper import Article
import requests
import markdown
import itertools
import datetime

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

import dateutil.parser
from dateutil import tz


# -----------------------------------------------------------------------------


def parse(url=None, html=None, text=None, title=None,
          sentences_count=5,
          options={},
          summarize_algo="luhn",
          date_timezone="America/New_York"):
    """
    Parse article to get relevant data

    :param url:
    :param html:
    :param text:
    :param title:
    :param sentences_count:
    :param options: {}
    :param summarize_algo:
    :param date_timezone: The timezone to convert the date to
    :return:
    """

    article = Article("")

    if text and title:
        article.is_parsed = True
        article.is_downloaded = True
        article.set_title(title)
        article.set_text(text)
    else:
        if url:
            r = requests.get(url.strip())
            if r.status_code != 200:
                raise Exception("Paper request failed '%s'" % url)
            html = r.content

        if html:
            soup = get_soup(html)
        else:
            raise Exception("Paper missing HTML content")

        article.set_html(remove_social_embeds(html))
        article.parse()
        article.nlp()

        if options.get("title_selector"):
            title = soup.select(options.get("title_selector"))
            if title:
                title = title[0].text
                article.set_title(title)

        if options.get("image_selector"):
            img = soup.select(options.get("image_selector"))
            if img:
                img = img[0].text
                article.set_top_img_no_check(img)

        if options.get("content_selector"):
            html = soup.select(options.get("content_selector"))
            if html:
                article.set_text(html[0].text)

    summary = summarize(text=article.text,
                        title=article.title,
                        algo=summarize_algo,
                        sentences_count=sentences_count)
    publish_date = article.publish_date
    if not publish_date and html:
        publish_date = extract_publish_date(html)
    if not publish_date:
        publish_date = datetime.datetime.now()

    return {
        "url": article.canonical_link,
        "title": article.title,
        "summary": summary,
        "summaries": summary.split("\n\n"),
        "text": article.text,
        "html": article.html,
        "top_image": article.top_image,
        "images": article.images,
        "videos": list(set(article.movies + extract_video_iframes(html))),
        "social_media_content": extract_social_media_content(html),
        "keywords": article.keywords,
        "tags": article.tags,
        "authors": article.authors,
        "published_date": datetime_to_local_timezone(publish_date),
        "md_text": ""
    }


def extract_page_links(url, selector, limit=10):
    """
    :returns list:
    """
    soup = get_url_soup(url)
    return [link["href"] for link in soup.select(selector)][:limit]

# -----------------------------------------------------------------------------


class FrequencySummarizer(object):

    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
         Initilize the text summarizer.
         Words that have a frequency term lower than min_cut
         or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') + list(punctuation))

    def _compute_frequencies(self, word_sent):
        """
          Compute the frequency of each of word.
          Input:
           word_sent, a list of sentences already tokenized.
          Output:
           freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        for w in freq.keys():
            freq[w] = freq[w]/m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq

    def summarize(self, text, n=5):
        """
          Return a list of n sentences
          which represent the summary of text.
        """
        sents = sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [sents[j] for j in sents_idx]

    def _rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)


def get_soup(html):
    return BeautifulSoup(html, "lxml")


def html_to_text(html):
    texts = get_soup(html).find_all(text=True)
    return "\n ".join(texts)


def get_url_soup(url):
    """
    Returns the beautiful object of url
    :param url:
    :return:
    """
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Paper request failed '%s'" % url)
    return get_soup(r.content)


SUMY_ALGO = {
    "luhn": LuhnSummarizer,  # Give out short Summary. Ideal for TLDR highlights
    # "edmundson": EdmundsonSummarizer,
    "lsa": LsaSummarizer,  # Second Best after Frequency
    "text-rank": TextRankSummarizer,
    "lex-rank": LexRankSummarizer,
}


def summarize(text, title=None, sentences_count=5, algo="frequency"):
    sentences = []
    language = "english"
    content = ""
    if title:
        content += title + ". "
    content += text
    content = content.replace("\r\n", "\n")

    if algo == "frequency":  # Best
        fs = FrequencySummarizer()
        sentences = fs.summarize(content, sentences_count)
    else:
        Summarizer = SUMY_ALGO[algo]
        parser = PlaintextParser.from_string(text, Tokenizer(language))
        stemmer = Stemmer(language)
        summarizer = Summarizer(stemmer)

        if algo == "edmundson":
            summarizer.bonus_words = parser.significant_words
            summarizer.stigma_words = parser.stigma_words

        summarizer.stop_words = get_stop_words(language)
        sentences = [str(sentence) for sentence in summarizer(
            parser.document, sentences_count)]

    return "\n\n".join(sentences)


def extract_social_media_content(html):
    if not html:
        return []

    embeds = []
    soup = get_soup(html)
    # Tweets
    for e in itertools.chain(soup.select('blockquote[class="twitter-tweet"]'),
                             soup.select('blockquote[class="instagram-media"]')):
        embeds.append(str(e))
    return embeds


def remove_social_embeds(html):
    soup = get_soup(html)
    bq = soup.find('blockquote')
    if bq:
        bq.decompose()
    return str(soup)


def extract_video_iframes(html):
    if not html:
        return []
    videos = []
    soup = get_soup(html)
    for i in soup.select('iframe[src*="youtube"]'):
        src = str(i.get("src"))
        videos.append(src)
    return videos


def extract_publish_date(html):
    if not html:
        return None

    soup = get_soup(html)
    meta_date = None
    for meta in soup.find_all("meta"):
        metaName = meta.get('name', '').lower()
        itemProp = meta.get('itemprop', '').lower()
        httpEquiv = meta.get('http-equiv', '').lower()

        if metaName in ["pubdate", "publishdate", "timestamp", "dc.date.issued",
                        "article:published_time", "date", "sailthru.date",
                        "article.published", "published-date", "article.created",
                        "article_date_original"]:
            meta_date = meta['content'].strip()
            break
        elif itemProp in ["datepublished", "datecreated"]:
            meta_date = meta['content'].strip()
        elif httpEquiv in ["date"]:
            meta_date = meta['content'].strip()
            break
    if meta_date:
        return dateutil.parser.parse(meta_date)

    return None


def datetime_to_local_timezone(dt, timezone="America/New_York", from_timezone="UTC"):
    """
    Fix datetime to local timezone
    :param dt: datetime object
    :param timezone:
    :param from_timezone:
    :return: datetime
    """
    from_zone = tz.gettz(from_timezone)
    to_zone = tz.gettz(timezone)
    dt = dt.replace(tzinfo=from_zone)
    return dt.astimezone(to_zone)
