
import time
import logging
from pickle import dumps, loads
from flasik import db, utils, ext, get_config


class NewsroomAuth(db.Model):

    """
    User
    """
    email=db.Column(db.EmailType, index = True, unique = True)
    password_hash=db.Column(db.String(255))
    name=db.Column(db.String(255))
    is_admin=db.Column(db.Boolean, default = False)
    is_active=db.Column(db.Boolean, default = True)
    last_login_at=db.Column(db.DateTime)
    secret_key=db.Column(db.String(255))
    refresh_token=db.Column(db.String(255))

    @classmethod
    def new(cls, email, password, name):
        """
        Create a new user
        :param email: str
        :param password: str
        :param name: str
        :return: User
        """

        email=email.strip().lower()
        if not utils.is_email_valid(email):
            raise Error("Invalid email")
        if not utils.is_password_valid(password):
            raise Error("Password is invalid")

        if cls.get_by_email(email):
            raise Error("Email address exists already")

        data={
            "email": email,
            "password_hash": cls.encrypt_password(password),
            "name": name,
            "is_active": True
        }
        user = cls.create(**data)
        return user

    @classmethod
    def encrypt_password(cls, password):
        return ext.crypto.hash_string(password)

    @classmethod
    def get_by_email(cls, email):
        """
        Return a User by email address
        """
        return cls.query().filter(cls.email == email).first()

    def change_email(self, email):
        """
        Change account email
        :param email:
        :param as_username
        :return: the email provided
        """
        email = email.strip().lower()
        data = {"email": email}
        if self.email != email:
            if self.get_by_email(email):
                raise Error("Email exists already")
            self.update(**data)

    def change_password(self, password):
        """
        Change the password.
        :param password:
        :return:
        """
        self.update(password_hash=self.encrypt_password(password))

        # Whenever the password is changed, reset the secret key to invalidate
        # any tokens in the wild
        self.reset_secret_key()

    def verify_password(self, password):
        """
        Check if the password matched the hash
        :returns bool:
        """
        return ext.crypto.verify_hashed_string(password, self.password_hash)

    def reset_secret_key(self):
        """
        Run this whenever there is a security change in the account.
        ie: password change.
        BTW, AuthUserLogin.change_password, already performs this method
        """
        self.update(secret_key=utils.guid())


class NewsroomSource(db.Model):
    """
    Source contains the source of the data
    With url and type
    """
    # Topic contains all the source of data
    TYPES = [('rss', 'RSS Feed'),  # A RSS feed
             ('youtube_channel', 'Youtube Channel'),  # A Youtube channel
             ('page_links', 'Page Links')  # A page containing links to query
             ]

    name = db.Column(db.String(255), index=True)
    type = db.Column(db.String(25), index=True)
    url = db.Column(db.String(255))
    # A query selector to select all links on page links
    page_links_selector = db.Column(db.String(255))
    limit = db.Column(db.Integer, default=30)  # the amount of content to fetch
    fetch_frequency = db.Column(db.Integer, default=60)  # In minutes
    last_fetched_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, index=True)

    @classmethod
    def new(cls, name, type, url,
            page_links_selector=None,
            fetch_frequency=60,
            is_active=True,
            limit=30
            ):
        return cls.create(name=name,
                          url=url,
                          type=type,
                          page_links_selector=page_links_selector,
                          fetch_frequency=fetch_frequency,
                          is_active=is_active,
                          limit=limit)

    def get_posts(self):
        return NewsroomPost.get_by_sources(self.id)

    def get_posts(self,
                  type=None,
                  order_by_published_date=False,
                  order_by_id=True):
        """
        Filter all posts of this feed
        :param type:
        :param order_by_published_date:
        :param order_by_id:
        :return:
        """
        posts = NewsroomPost.get_posts(type=type,
                                       order_by_published_date=order_by_published_date,
                                       order_by_id=order_by_id)

        posts = posts.filter(NewsroomPost.source_id.in_(set([self.id])))
        return posts

    @property
    def total_posts(self):
        posts = NewsroomPost.query().filter(NewsroomPost.source_id.in_(set([self.id])))
        return posts.count()

    @property
    def should_fetch(self):
        """
        Check if this source should be fetched
        :returns bool:
        """
        if not self.last_fetched_at:
            return True
        return self.last_fetched_at.replace(minutes=+self.fetch_frequency) < db.utcnow()

    def hit_fetch(self):
        """
        Update the last fetched date
        """
        self.update(last_fetched_at=db.utcnow())

    def to_dict(self):
        d = super(self.__class__, self).to_dict()
        d["total_posts"] = self.total_posts
        return d


class NewsroomFeed(db.Model):
    """
    Feeds aggregate sources
    """
    name = db.Column(db.String(255), index=True)
    description = db.Column(db.String(255))
    is_nsfw = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)

    @classmethod
    def new(cls, name, description="", is_nsfw=False, is_active=True):
        return cls.create(name=name,
                          description=description,
                          is_active=is_active,
                          is_nsfw=is_nsfw)

    def add_source(self, id):
        NewsroomFeedMap.add(source_id=id, feed_id=self.id)

    def remove_source(self, id):
        NewsroomFeedMap.remove(source_id=id, feed_id=self.id)

    def get_posts(self,
                  type=None,
                  order_by_published_date=False,
                  order_by_id=True):
        """
        Filter all posts of this feed
        :param type:
        :param order_by_published_date:
        :param order_by_id:
        :return:
        """
        posts = NewsroomPost.get_posts(type=type,
                                       order_by_published_date=order_by_published_date,
                                       order_by_id=order_by_id)

        ids = [m.source.id for m in self.sources]
        posts = posts.filter(NewsroomPost.source_id.in_(set(ids)))
        return posts

    @property
    def total_posts(self):
        ids = [m.source.id for m in self.sources]
        posts = NewsroomPost.query().filter(NewsroomPost.source_id.in_(set(ids)))
        return posts.count()

    @property
    def total_sources(self):
        return len(self.sources)

    def update_sources(self, sources_list=[]):
        """
        Replace the sources list with the new list.
        sources_list must contain items to be retained and new items
        if a sources is omitted, it will be removed
        :param sources_list list:
        """
        [NewsroomFeedMap.remove(feed_id=self.id, source_id=s.source_id) for s in self.sources]
        [NewsroomFeedMap.add(feed_id=self.id, source_id=s) for s in sources_list]

    def get_sources(self):
        return [source for source in self.sources if source.source.is_deleted is False]

    def list_sources(self):
        """
        Return the dict of all sources in a list
        """
        return [m.source.to_dict() for m in self.get_sources()]

    def to_dict(self):
        d = super(self.__class__, self).to_dict()
        d["total_posts"] = self.total_posts
        d["total_sources"] = self.total_sources
        d["sources_ids"] = [s.source_id for s in self.get_sources()]
        return d


class NewsroomFeedMap(db.Model):
    source_id = db.Column(db.Integer, db.ForeignKey(NewsroomSource.id))
    feed_id = db.Column(db.Integer, db.ForeignKey(NewsroomFeed.id))
    source = db.relationship(NewsroomSource)
    feed = db.relationship(NewsroomFeed, backref="sources")

    @classmethod
    def add(cls, source_id, feed_id):
        c = cls.query().filter(cls.source_id == source_id) \
            .filter(cls.feed_id == feed_id) \
            .first()
        if not c:
            cls.create(source_id=source_id, feed_id=feed_id)

    @classmethod
    def remove(cls, source_id, feed_id):
        c = cls.query().filter(cls.source_id == source_id) \
            .filter(cls.feed_id == feed_id) \
            .first()
        if c:
            c.delete(hard_delete=True)


class NewsroomPost(db.Model):
    POST_TYPES_MAP = {
        "article": "news",
        "text": "news",
        "video": "videos",
        "gallery": "photos",
        "image": "photos"
    }

    POST_TYPES_TITLE_MAP = {
        "news": "News",
        "articles": "News",
        "videos": "Videos",
        "photos": "Photos",
        "all": "All"
    }

    CONTENT_GROUP = {
        "news": ["article", "text"],
        "articles": ["article", "text"],
        "videos": ["video"],
        "photos": ["gallery", "image"],
        "photos_videos": ["video", "gallery", "image"],
        "all": ["article", "text", "video", "gallery", "image"]
    }
    CONTENT_GROUP_TITLE = {
        "news": "News",
        "articles": "Articles",
        "videos": "Videos",
        "photos": "Photos",
        "all": "All"
    }

    source_id = db.Column(db.Integer, db.ForeignKey(NewsroomSource.id))
    url = db.Column(db.String(255))
    hash_key = db.Column(db.String(32), index=True, unique=True)
    domain = db.Column(db.String(255), index=True)
    is_nsfw = db.Column(db.Boolean, default=False, index=True)

    type = db.Column(db.String(25), index=True)
    slug = db.Column(db.String(255), index=True)
    title = db.Column(db.Text)
    title_alt = db.Column(db.Text)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    content_original_text = db.Column(db.Text)
    keywords = db.Column(db.JSONType)

    # Store image in StorageObject
    image = db.Column(db.StorageObjectType)
    # Save the image as string alternative
    image_url = db.Column(db.String(255))
    # image source
    image_src = db.Column(db.Text)

    images = db.Column(db.JSONType)
    videos = db.Column(db.JSONType)
    authors = db.Column(db.JSONType)

    article_published_date = db.Column(db.DateTime)

    has_embed = db.Column(db.Boolean, default=False)
    embed_url = db.Column(db.Text)

    # Social media embeds
    social_media_content = db.Column(db.JSONType)

    # Archive post should no longer by displayed in the list, but can be searched
    is_archived = db.Column(db.Boolean, index=True, default=False)
    archived_at = db.Column(db.DateTime)

    source = db.relationship(NewsroomSource, backref="posts")

    @classmethod
    def hash_key_exists(cls, hash_key):
        s = cls.query(include_deleted=True)\
            .filter(cls.hash_key == hash_key)\
            .first()
        return True if s else False

    @classmethod
    def make_hash_key(cls, url, source_id):
        c = "%s:%s" % (source_id, url)
        return utils.md5(c)

    @classmethod
    def new(cls, **kwargs):
        kwargs["hash_key"] = cls.make_hash_key(source_id=kwargs.get("source_id"),
                                               url=kwargs["url"])
        title = kwargs.get("title")
        if not title:
            title = str(utc_now())
        kwargs["slug"] = cls.create_slug(title)
        return cls.create(**kwargs)

    @classmethod
    def get_by_sources(cls,
                       ids,
                       nsfw=None,
                       type=None,
                       order_by_published_date=False,
                       order_by_id=True):
        if not isinstance(ids, list):
            ids = [ids]

        posts = cls.get_posts(
                              type=type,
                              order_by_published_date=order_by_published_date,
                              order_by_id=order_by_id)

        posts = posts.filter(cls.source_id.in_(set(ids)))
        return posts

    @classmethod
    def get_posts(cls,
                  type=None,
                  content_group=None,
                  order_by_published_date=False,
                  order_by_id=True,
                  include_archived=False
                  ):
        """

        :param nsfw:
        :param type:
        :param content_group: (string)
        :param order_by_published_date:
        :param order_by_id:
        :param include_archived:
        :return:
        """
        q = cls.query()

        if content_group and content_group in cls.CONTENT_GROUP:
            type = cls.CONTENT_GROUP[content_group]

        if type:
            if not isinstance(type, list):
                type = [type]
            q = q.filter(cls.type.in_(type))

        elif order_by_published_date:
            q = q.order_by(cls.article_published_date.desc())
        elif order_by_id:
            q = q.order_by(cls.id.desc())

        if not include_archived:
            q = q.filter(cls.is_archived == False)

        return q

    @classmethod
    def archive_posts(cls, months=1, types=["article"]):
        """
        Archive all posts
        :param months:
        :param types: list of types
        :return:
        """
        t = datetime.datetime.now() - datetime.timedelta(
            days=(months * 365) / 12)
        types = [types] if not isinstance(types, list) else types

        cls.query(cls.id,
                  cls.is_archived,
                  cls.archived_at,
                  cls.type,
                  cls.created_at) \
            .filter(cls.is_archived == False) \
            .filter(cls.created_at < t) \
            .filter(cls.type.in_(types)) \
            .update({"is_archived": True,
                     "archived_at": utc_now()
                     }, synchronize_session=False)
        cls.db.commit()

    @classmethod
    def create_slug(cls, title):
        slug = None
        slug_counter = 0
        _slug = utils.slugify(title).lower()
        while True:
            slug = _slug
            if slug_counter > 0:
                slug += str(slug_counter)
            slug_counter += 1
            if not cls.get_by_slug(slug):
                break
        return slug

    @classmethod
    def get_by_slug(cls, slug):
        """
        Return a post by slug
        """
        return cls.query().filter(cls.slug == slug).first()

    @property
    def published_date(self):
        return self.article_published_date \
            if self.type in ["video"] \
            else self.created_at

    @property
    def article_videos(self):
        """
        Return a list of all the videos on this article.
        Will also format the Youtube url for OEmbed
        """
        videos = []
        if self.videos:
            _videos = self.videos
            for url in _videos:
                if "youtube" in url:
                    url = youtube.watch_url(url=url)
                videos.append(url)
        return videos

    @property
    def slug_url(self):
        post_type = self.POST_TYPES_MAP.get(self.type)
        return "/%s/%s/" % (post_type, self.slug)

    def archive(self, archive=True):
        data = {
            "is_archived": archive,
            "archived_at": utc_now() if archive else None
        }
        self.update(**data)

    def set_slug(self, title):
        slug = utils.slugify(title)
        if title and slug != self.slug:
            slug = self.create_slug(slug)
            self.update(slug=slug)

    @property
    def post_type(self):
        return self.POST_TYPES_MAP.get(self.type)

    def to_dict(self):

        d = super(self.__class__, self).to_dict()
        d["slug_url"] = self.slug_url
        d["article_videos"] = self.article_videos
        d["published_date"] = self.published_date
        d["post_type_name"] = self.POST_TYPES_TITLE_MAP.get(self.post_type)
        d["post_type"] = self.post_type

        return d


class NewsroomTaskQueue(db.Model):
    """
    A poor man task queue system to process messages
    Tasks are categorized by name, to be retrieved and processed accordingly
    It uses the FIFO process and messages can be lost
    example:

    def fn(data):
        ...

    NewsroomTaskQueue.add(name="MyQName", callback=fn, data={})

    # run in background 
    NewsroomTaskQueue.run(name="MyQName", size=5)
    """

    name = db.Column(db.String(255), index=True)
    message = db.Column(db.Text)
    DEFAULT_NAME = "NEWSROOM"

    @classmethod
    def add(cls, callback, name=None, *args, **kwargs):
        """
        Add a message to be process later on by @run
        :param name: the name of the queue
        :callback: function to process *args and **kwargs
        """
        data = {
            'callback': callback,
            'args': args,
            'kwargs': kwargs
        }
        name = cls.DEFAULT_NAME if name is None else name
        cls.create(name=name, message=dumps(data))
        logging.info("Task Queue: new message added in '%s'" % name)

    @classmethod
    def pull(cls, name=None, size=5):
        """
        Pull and delete retrieved messages.
        **Messages could be lost if an error occur
        """
        name = cls.DEFAULT_NAME if name is None else name
        messages = []
        for m in cls.query().filter(cls.name == name).order_by(cls.id.asc()).limit(size):
            messages.append(m.message)
            m.delete(hard_delete = True)
        return messages

    @classmethod
    def run(cls, name=None, size=5, pause=120, once=False):
        """
        Run the QUEUED worker. If pool is provided, it will use
        :param name: the name of the queue
        :param size: The maximum number of messages to read from the queue
        :param pause: The pause time between each request
        :param once: If true, it will run once
        :return:
        """
        name = cls.DEFAULT_NAME if name is None else name
        while True:
            logging.info("Task Queue: running queue in '%s' ..." % name)
            for message in cls.pull(name=name, size=size):
                try:
                    body = loads(message)
                    callback = body.get("callback")
                    callback(*body.get("args"), **body.get("kwargs"))
                except Exception as ex:
                    logging.error("Failed running task: '%s'" % ex.message)
            if once:
                break
            time.sleep(pause)

