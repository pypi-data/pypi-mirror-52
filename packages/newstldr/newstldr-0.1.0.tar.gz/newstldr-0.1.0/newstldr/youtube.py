from six.moves.urllib.parse import urlparse, parse_qs
import requests
import datetime

WATCH_URL = "https://www.youtube.com/watch?v="
EMBED_URL = "https://www.youtube.com/embed/"
EMBED_V_URL = "https://www.youtube.com/v/"

def extract_id_from_url(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def embed_url(code=None, url=None, v=False):
    """
    :param code: code
    :param url: url
    :return:
    """
    if not code and url:
        code = extract_id_from_url(url)
    return (EMBED_V_URL if v else EMBED_URL) + code

def watch_url(code=None, url=None):
    """
    :param code: code
    :param url: url
    :return:
    """
    if not code and url:
        code = extract_id_from_url(url)
    return WATCH_URL + code

class Youtube(object):
    API_URL = 'https://www.googleapis.com/youtube/v3'

    def __init__(self, key=None):
        self.key = key

    def init_app(self, app):
        self.key = app.config.get("GOOGLE_API_KEY")

    def video(self, id=None, url=None):
        """
        Get the video info by id or url

        :param id:
        :return:
        """
        if url and not id:
            id = extract_id_from_url(url)

        params = {
            "key": self.key,
            "part": "snippet",
            "id": ",".join(id) if isinstance(id, list) else id
        }
        api_url = self.API_URL + "/videos"
        results = requests.get(api_url, params=params)
        if results.status_code == 200:
            data = results.json()
            for item in data["items"]:
                if id == item["id"]:
                    return self._parse_video_item(id, item)
        return None

    def channel(self, id, limit=10, order="date"):
        """
        Get channel
        :param id:
        :param limit:
        :return:
        """
        return self.search(channelId=id, limit=limit, order=order)

    def search(self, **kwargs):
        kwargs["key"] = self.key
        kwargs["part"] = "snippet"
        kwargs["maxResults"] = 50
        limit = kwargs.pop("limit", 50)
        if limit < kwargs["maxResults"]:
            kwargs["maxResults"] = limit

        url = self.API_URL + "/search"
        videos = []
        while True:
            try:
                results = requests.get(url, params=kwargs)
                if results.status_code == 200:
                    data = results.json()
                    for item in data["items"]:
                        id = item["id"]["videoId"]
                        videos.append(self._parse_video_item(id, item))
                    kwargs["pageToken"] = data["nextPageToken"]
                    if len(videos) >= limit:
                        break
                else:
                    break
            except KeyError:
                break
        return videos

    def playlist(self, id):
        pass

    def format_utc_date(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _parse_video_item(self, id, item):
        return {
            "id": id,
            "url": watch_url(id),
            "embed": embed_url(id),
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "thumbnail": self._select_thumbnail(item["snippet"]["thumbnails"]),
            "published_date": self.format_utc_date(item["snippet"]["publishedAt"])
        }

    def _select_thumbnail(self, thumbnails):
        """
        To select the highest resolution available
        Some thumbnail may not have maxres, so we'll go down the path
        :param thumbnails:
        :return: string
        """
        for res in ["maxres", "standard", "high", "medium", "default"]:
            if res in thumbnails:
                return thumbnails[res]["url"]