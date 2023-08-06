

from flasik import (Flasik,
                    set_page_context,
                    get_config,
                    abort,
                    g,
                    ext,
                    url_for,
                    redirect,
                    models,
                    request,
                    response,
                    functions,
                    utils)
import flasik
from flask import request as f_request
import core
import markdown

# ------------------------------------------------------------------------------


class BaseAPI(object):

    def before_request(self, page, *a, **kw):
        self._page = int(f_request.args.get("page", 1))
        self._per_page = int(f_request.args.get("per_page", 10))
        self.auth_id = None
        self.request_data = None

        # JWT
        try:
            jwt = request.get_auth_bearer()
            auth = ext.crypto.jwt_decode(jwt)
            if auth and auth["id"]:
                self.auth_id = auth["id"]
        except Exception as e:
            pass

        # Request Data
        if request.is_post():
            content_type = f_request.headers.get('Content-Type')
            if 'application/json' in content_type.lower():
                self.request_data = f_request.json["data"]

        # All method POST are required to have auth_id
        if page not in ["token", "register"] and request.is_post():
            if not self.auth_id:
                # Temporary CORS fix for errors
                headers = {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'DELETE, GET, POST, PUT',
                    'Access-Control-Allow-Headers': f_request.headers.get('Access-Control-Request-Headers')
                }
                code = 403
                response = {
                    "error": True,
                    "code": code,
                    "message": "Unauthorize. Invalid token"
                }
                return self._403("Unauthorize. Invalid token"), headers
                return response, code, headers

    def _400(self, message="Bad Request"):
        return self._error(message, 400)

    def _401(self, message="Unauthorize"):
        return self._error(message, 401)

    def _403(self, message="Forbidden"):
        return self._error(message, 403)

    def _404(self, message="Not Found"):
        return self._error(message, 404)

    def _resp(self, data={}, pagination=None):
        resp = {
            "data": data
        }
        return resp

    def _error(self, message=None, code=400):
        return {
            "error": True,
            "message": message,
            "code": code
        }, code


@request.route("/newstldr/auth")
class Auth(BaseAPI, Flasik):

    def _gen_jwt_token(self):
        pass

    def _format_user(self, user):
        u = user.to_dict()
        del u["password_hash"]
        del u["secret_key"]
        del u["refresh_token"]
        return u 

    @response.cors()
    @response.json
    @request.csrf_exempt
    @request.post
    def token(self):
        content_type = f_request.headers.get('Content-Type')

        if 'application/json' in content_type.lower():
            _data = f_request.json["data"]

            email = _data.get("email")
            password = _data.get("password")
            user = models.NewsroomAuth.get_by_email(email)
            if not user or not user.verify_password(password) or not user.is_active:
                return self._401()

            ttl = 60*24
            return {
                "refres_token": None,
                "access_token": ext.crypto.jwt_encode({"id": user.id}, expires_in=ttl)
            }

    @response.cors()
    @request.csrf_exempt
    @request.post_get
    def account(self):
        """
        To admin own account
        """
        if self.auth_id:
            user = models.NewsroomAuth.get(self.auth_id)
            if user and user.is_active:
                if request.is_post():
                    if self.request_data:
                        _data = self.request_data

                        # __ACTION__
                        action = _data.get("__ACTION__")

                        # CHANGE_EMAIL
                        if action == "CHANGE_EMAIL":
                            verify_password = _data.get("verif_password")
                            email = _data.get("new_email")
                            if not user.verify_password(verify_password):
                                return self._400("Invalid password")                            
                            elif not utils.is_email_valid(email):
                                return self._400("Invalid email")
                            elif models.NewsroomAuth.get_by_email(email):
                                return self._400("Email exists already")
                            else:
                                user.change_email(email)

                        # CHANGE_PASSWORD
                        elif action == "CHANGE_PASSWORD":
                            verify_password = _data.get("verif_password")
                            password = _data.get("new_password")
                            conf_password = _data.get("confirm_password")
                            if not user.verify_password(verify_password):
                                return self._400("Invalid password")
                            elif password != conf_password or not utils.is_password_valid(password):
                                return self._400("Invalid password or passwords don't match")
                            else:
                                user.change_password(password)

                        # CHANGE_NAME
                        elif action == "CHANGE_NAME":
                            name = _data.get("name")
                            if name:
                                user.update(name=name)

                return self._resp(self._format_user(user))

        return self._403()

    @response.cors()
    @request.csrf_exempt
    @request.post
    def register(self):
        """
        Register as admin 
        """
        query = models.NewsroomAuth.query()
        has_admin = True if query.count() else False  

        if not has_admin and request.is_post():
            if self.request_data:
                _data = self.request_data

                # __ACTION__
                action = _data.get("__ACTION__")

                # CHANGE_EMAIL
                if action == "REGISTER":
                    name = _data.get("name")
                    email = _data.get("email")
                    password = _data.get("password")
                    conf_password = _data.get("confirm_password")
                    if not name:
                        return self._400("Invalid Name")                    
                    elif not utils.is_email_valid(email):
                        return self._400("Invalid email")
                    elif models.NewsroomAuth.get_by_email(email):
                        return self._400("Email exists already")
                    elif password != conf_password or not utils.is_password_valid(password):
                        return self._400("Invalid password or passwords don't match")
                    else:
                        user = models.NewsroomAuth.new(email=email, password=password, name=name)
                        if user:
                            user.update(is_admin=True)
                            return self._resp({
                                "registered": True
                            })

        return self._403()

    @response.cors()
    @request.csrf_exempt
    @request.post_get
    def users(self):
        """
        Admin other users account. only user with is_admin = True
        """
        if self.auth_id:
            admin = models.NewsroomAuth.get(self.auth_id)
            if admin and admin.is_active and admin.is_admin:
                content_type = f_request.headers.get('Content-Type')
                if 'application/json' in content_type.lower():
                    _data = f_request.json["data"]
                    action = _data.get("__ACTION__")

        return self._403()


@request.route("/newstldr")
class News(BaseAPI, Flasik):

    def _md_to_html(self, content):
        return

    def _format_post(self, post):
        return {
            "id": post.id,
            "title": post.title_alt if post.title_alt else post.title,
            "domain": post.domain,
            "type": post.type,
            "slug": post.slug,
            "content": post.summary,
            "content_html": markdown.markdown(post.summary) if post.summary else '',
            "description": post.description,
            "keywords": post.keywords,
            "image": post.image_url,
            "published_date": post.published_date,
            "social_media_content": post.social_media_content,
            "authors": post.authors,
            "created_at": post.created_at,
            "source_id": post.source_id,
            "ref_url": post.url
        }

    def _posts_results(self, query):
        limit = 300
        posts = query.limit(limit)
        results = posts.paginate(per_page=self._per_page, page=self._page)
        data = [self._format_post(post) for post in results]
        if len(data) == 0:
            return self._404()
        return {
            "data": data,
            "per_page": results.per_page,
            "total_pages": results.total_pages,
            "page": results.page,
            "total_items": results.total_items
        }

    @response.cors()
    @response.json
    def app_status(self):
        query = models.NewsroomAuth.query()        
        return self._resp({
            "ping": True,
            "registered": True if query.count() else False 
        })        


    @response.cors()
    @response.json
    @request.csrf_exempt
    @request.route('/sources/', methods=["GET"], endpoint="ALL_SOURCES", defaults={"id": None})
    @request.route('/sources/', methods=["POST"], endpoint="NewSource")
    @request.route('/sources/<int:id>/', methods=["POST", "GET"])
    def sources(self, id=None):
        # GET
        if request.is_get():
            if id:
                entry = models.NewsroomSource.get(id)
                if not entry:
                    return self._404()
                return self._resp(entry.to_dict())
            else:
                sources = [s.to_dict() for s in models.NewsroomSource.query()]
                return self._resp(sources)

        # UPDATE
        elif request.is_post():
            if self.request_data:
                _data = self.request_data

                # __ACTION__
                action = _data.get("__ACTION__")
                if action:
                    if not id:
                        return self._404()
                    entry = models.NewsroomSource.get(id)
                    if not entry:
                        return self._404()
                    if action == 'DELETE':
                        entry.delete()
                    return {}

                # -->> Update/Create
                name = _data.get("name")
                type_ = _data.get("type")
                url = _data.get("url")

                if not name or not type_ or not url:
                    return self._error(message="Unable to update. Missing name or type or url", code=400)

                data = {
                    "name": name,
                    "type": type_,
                    "url": url,
                    "page_links_selector": _data.get("page_links_selector"),
                    "is_active": _data.get("is_active", True),
                    "limit": _data.get("limit", 30),
                    "fetch_frequency": _data.get("fetch_frequency", 60),
                }
                entry = None
                if id:
                    entry = models.NewsroomSource.get(id)
                    if entry:
                        entry.update(**data)
                else:
                    entry = models.NewsroomSource.new(**data)
                return self._resp(entry.to_dict())

        return self._error("Invalid request")

    @response.cors()
    @response.json
    @request.csrf_exempt
    @request.route('/feeds/', methods=["GET"], endpoint="ALL_FEEDS")
    @request.route('/feeds/', methods=["POST"], endpoint="NEW_FEED")
    @request.route('/feeds/<int:id>/sources/', methods=["GET"], endpoint="FEEDS_SOURCES", defaults={"list_sources": True})
    @request.route('/feeds/<int:id>/posts/', methods=["GET"], endpoint="FEEDS_POSTS", defaults={"list_posts": True})
    @request.route('/feeds/<int:id>/', methods=["POST", "GET"])
    def feeds(self, id=None, list_sources=False, list_posts=False):
        """
        Feeds admin
        """

        # Get
        if request.is_get():
            if id:
                entry = models.NewsroomFeed.get(id)
                if not entry:
                    return self._404()

                # list sources
                if list_sources:
                    return self._resp(entry.list_sources())

                # list posts
                elif list_posts:
                    return self._posts_results(entry.get_posts())

                else:
                    return self._resp(entry.to_dict())
            else:
                # Show all feeds
                feed = [f.to_dict() for f in models.NewsroomFeed.query()]
                return self._resp(feed)

        # UPDATE:POST
        elif request.is_post():
            if self.request_data:
                _data = self.request_data

                # __ACTION__
                action = _data.get("__ACTION__")
                if action:
                    if not id:
                        return self._404()
                    entry = models.NewsroomFeed.get(id)

                    if not entry:
                        return self._404()

                    if action == 'DELETE':
                        entry.delete()

                    elif action == "UPDATE_SOURCES":
                        sources_ids = _data.get("sources_ids")

                        if type(sources_ids) != list:
                            return self._error(message="Unable to update sources. Invalid sources_ids type", code=400)

                        entry.update_sources(sources_ids)
                        return self._resp(entry.to_dict())
                    return {}

                # -->> Update/Create
                name = _data.get("name")

                if not name:
                    return self._error(message="Unable to update. Missing name", code=400)

                data = {
                    "name": name,
                    "description": _data.get("description"),
                    "is_active": _data.get("is_active", True),
                    "is_nsfw": _data.get("is_nsfw", False),
                }
                entry = None
                if id:
                    entry = models.NewsroomFeed.get(id)
                    if entry:
                        entry.update(**data)
                else:
                    entry = models.NewsroomFeed.new(**data)
                return self._resp(entry.to_dict())

        return self._error("Invalid request")

    @response.cors()
    @response.json
    @request.csrf_exempt
    @request.route('/posts/', methods=["GET"], endpoint="ALL_POSTS")
    @request.route('/posts/<int:id>/', methods=["GET", "POST"])
    def posts(self, id=None):

        if id is None and request.is_get():
            posts = models.NewsroomPost.get_posts()
            return self._posts_results(posts)

        elif id and (request.is_get() or request.is_post()):
            post = models.NewsroomPost.get(id)
            if not post:
                return self._404()

            if request.is_get():
                return {
                    "data": self._format_post(post)
                }

            elif request.is_post():
                if self.request_data:
                    _data = self.request_data

                    # __ACTION__
                    action = _data.get("__ACTION__")
                    if action == "DELETE":
                        post.delete()
                        return {}

        return self._error("Invalid request")
