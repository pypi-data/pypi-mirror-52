"""
NewsTLDR

Newsroom is an aggregator that summarize the news

"""

import re
import os
import datetime
import hashlib
import json
import logging
import uuid
import urllib
import redis
from flasik import (Flasik,
                    db,
                    get_config,
                    url_for,
                    redirect,
                    models,
                    request,
                    response,
                    functions,
                    utils)
import flasik
import arrow
import feedparser
from . import (article_parser, youtube, imagesize)
from sqlalchemy import exc

__version__ = "0.1.0"

# register_package(__name__)


SUMMARIZE_MAX_SENTENCES = 5
ARTICLE_IMAGE_MIN_WIDTH = 400
ARTICLE_IMAGE_REJECT_LOGO_KEYWORDS = ["logo"]

CWD = os.path.dirname(__file__)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Youtube
yt = youtube.Youtube()

@flasik.extends
def _initialize(app):
    """
    Initialize all configs
    """
    yt.key = get_config("NTLDR_GOOGLE_API_KEY")


# -----
# Import Sources

def import_sources():
    """
    Import all topics from the DB
    :return:
    """
    for source in models.NewsroomSource.query():

        if source.is_active and source.should_fetch:
            source.hit_fetch()

            if source.type == "rss":
                _import_rss_feed(url=source.url, source_id=source.id)

            elif source.type == "youtube_channel":
                _import_youtube_channel(url=source.url, source_id=source.id)

            elif source.type == "page_links":
                _import_page_links(
                    url=source.url, source_id=source.id, selector=source.page_links_selector)


def _import_url(url, source_id, post_type=None, options={}):
    """
    To import a url
    :param url:
    :param source_id:
    :param post_type:
    :param options:
    """
    if not post_type:
        url, post_type = get_url_type(url)

    data = {
        "type": post_type,
        "source_id": source_id,
        "url": url,
        "_options": options
    }
    task_save_post(data)


def _import_rss_feed(url, source_id, limit=10):
    """ Import RSS FEED 
    :param url: feed_url
    """
    feed = feedparser.parse(url)
    if feed:
        for item in feed.entries[:limit]:
            try:
                _import_url(url=item.link,
                            source_id=source_id,
                            post_type="article")
            except Exception as ex:
                pass


def _import_page_links(url, source_id, selector, limit=10):
    for link in article_parser.extract_page_links(url, selector, limit=limit):
        _import_url(url=link,
                    source_id=source_id,
                    post_type="article")


def _import_youtube_channel(url, source_id, limit=10):
    """ Import Youtube channel videos 
    :param url: channel_id
    """
    for video in yt.channel(url, limit=limit):
        data = {
            "type": "video",
            "source_id": source_id,
            "title": video["title"],
            "url": video["url"],
            "image_src": video["thumbnail"],
            "article_published_date": video["published_date"],
            "content": video["description"],
        }
        task_save_post(data)

# --------
# Tasks

# Task: Save Post


def task_save_post(data):
    """
    A shortcut to save
    :param data:
    :return:
    """
    if post_hash_key_exists(url=data["url"], source_id=data["source_id"]):
        logging.warn('Skipping: Hash key exist for: %s' % data["url"])
        return
    logging.info("Queue post: %s" % data["url"])
    models.NewsroomTaskQueue.add(callback=_save_post, data=data)
    #_save_post(data)


def _save_post(data):
    """
    Save post
    :params data: dict
    return post
    """
    try:

        _options = data.pop("_options", {})
        image_src = None
        if post_hash_key_exists(url=data["url"], source_id=data["source_id"]):
            logging.warn("Skipping: cache key exists for : %s" % data["url"])
            return

        # Article are more restrictive
        if data["type"] in ["article", "site"]:
            article_data = parse_article_url(data["url"], options=_options)
            # no data
            if not article_data:
                logging.warn("Skipping: article data is empty: %s" %
                             data["url"])
                return

            data.update(article_data)

        # parse_article_url still can change the type. So making sure
        # it's not a video
        if data["type"] != "video":
            # Articles must have images and be more than 600px
            if not data.get("image_src"):
                logging.warn('Skipping: article without top-image')
                return

            # If the image contain keywords to be rejected
            if utils.in_any_list(ARTICLE_IMAGE_REJECT_LOGO_KEYWORDS, data.get("image_src")):
                logging.warn('Skipping: image has rejected keywords in name')
                return

            # Try to rewrite the image, if it needs to be reformatted
            img_rw_pat = _options.get("image_rewrite_pattern", "")
            img_re_rep = _options.get("image_rewrite_replacement", "")
            data["image_src"] = rewrite_image_url(url=data["image_src"],
                                                  pat=img_rw_pat,
                                                  rep=img_re_rep)

            img_size = imagesize.from_url(data.get("image_src"))
            if not img_size or img_size[0] < ARTICLE_IMAGE_MIN_WIDTH:
                logging.warn("Skipping: Image size doesn't fit", data.get("image_src"), img_size)
                return

        image_src = data.get("image_src")

        if data["type"] == "image":
            image_src = data["url"]

        if "url" in data:
            data["domain"] = get_domain(data["url"])

        if not data.get("article_published_date"):
            data["article_published_date"] = arrow.utcnow()

        # Only with image we can save
        if image_src: 
            img = None
            try: 
                post = models.NewsroomPost.new(**data)
                img = save_image(image_src)
                if img:
                    post.update(image=img, image_url=img.url)
                    return post
                else:
                    post.delete(hard_delete=True)
            except exc.IntegrityError as ie:
                if img: 
                    img.delete()
    except Exception as ex2:
        logging.exception(ex2)


# Archive posts
def task_archive_posts():
    models.NewsroomTaskQueue.add(callback=_archive_posts)


def _archive_posts():
    models.NewsroomPost.archive_posts(months=1, types=["article"])


# -------------


def get_domain(url):
    parse_uri = utils.urlparse(url)
    return parse_uri.hostname


def rewrite_image_url(url, pat, rep):
    """
    To rewrite the image url, based on regexp pattern
    :param url: the url
    :param pat: pattern to replace
    :param rep: What to replace the pattern with
    :return: string
    """
    return re.sub(pat, rep, url)


def get_image_ext(url):
    """
    returns string
    """
    ext = os.path.splitext(url.split("?")[0])[
        1][1:].lower().replace("jpeg", "jpg")
    return ext if ext in ["png", "gif", "jpg"] else None


def save_image(url, **kwargs):
    """
    Save images
    :param url:
    :return:
    """
    image_path = None
    try:
        ext = get_image_ext(url)
        if ext:
            prefix = get_config("NTLDR_IMAGES_STORAGE_PREFIX")
            name = str(uuid.uuid4().hex)
            image_path = "/tmp/%s.%s" % (name, ext)
            urllib.urlretrieve(url, image_path)
            meta_data = {
                'Cache-Control': 'max-age=604800',  # 7 days
            }
            name += "." + ext
            return functions.storage.upload(image_path,
                                            name=name,
                                            prefix=prefix,
                                            public=True,
                                            meta_data=meta_data)
        raise ValueError('Invalid image extension: %s' % ext)
    except Exception as ex:
        logging.exception(ex)
    finally:
        if image_path and os.path.isfile(image_path):
            os.remove(image_path)
    return None

def get_url_type(url):
    """
    Try to guess a URL type 
    Returns the url and the type of the url
    :param url:
    :return tuple: (url, type)
    """
    _extension = url.split(".")[-1].lower()
    _type = "site"
    if _extension in ['jpg', 'jpeg', 'gif', 'png', 'bmp']:  # gifv
        _type = "image"
    elif utils.in_any_list(["//imgur.com/a/", "//imgur.com/gallery/"], url):
        _type = "gallery"
    elif "twitter.com/status/" in url:
        _type = "tweet"
    elif "instagram.com/p/" in url:
        _type = "instagram"
    elif utils.in_any_list(["youtube", "vimeo", "youtu.be"], url):
        _type = "video"
    return url, _type


def parse_article_url(url, options={}):
    """
    Parse an article and insert the necessary info

    :param url:
    :param options:
    :return:
    """
    data = {}
    article = article_parser.parse(url=url, options=options)

    # Some articles may contain more social embed than content
    # so we're considering it as full article
    if len(article["summaries"]) >= SUMMARIZE_MAX_SENTENCES \
            or len(article["social_media_content"]) > 0 \
            or len(article["videos"]) > 0:

        # Embed youtube video
        video = None
        for embed_url in article["videos"]:
            if "youtube" in embed_url:
                video = yt.video(url=embed_url)
                if video:
                    data.update({
                        "has_embed": True,
                        "embed_url": video["url"]
                    })
                    break

        # Change article to a video
        if len(article["summaries"]) < SUMMARIZE_MAX_SENTENCES \
                and "has_embed" in data \
                and "youtube" in data["embed_url"]\
                and video:
            data = {
                "title": video["title"],
                "type": "video",
                "url": data["embed_url"],
            }
        elif len(article["summaries"]) >= SUMMARIZE_MAX_SENTENCES:
            data.update({
                "url": article["url"],
                "title": article["title"],
                "content": article["text"],
                "summary": article["summary"],
                "description": article["summaries"][0],
                "image_src": article["top_image"],
                "images": article["images"],
                "videos": article["videos"],
                "keywords": article["keywords"],
                "social_media_content": article["social_media_content"],
                "authors": article["authors"],
                "article_published_date": article["published_date"]
            })
        else:
            data = {}
    return data


def post_hash_key_exists(url, source_id):
    hash_key = models.NewsroomPost.make_hash_key(url=url, source_id=source_id)
    return models.NewsroomPost.hash_key_exists(hash_key)
