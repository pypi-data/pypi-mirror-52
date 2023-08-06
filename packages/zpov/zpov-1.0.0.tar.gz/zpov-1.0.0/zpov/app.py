from typing import Any, Optional
import nacl.exceptions
import nacl.pwhash
import jinja2
import pygit2

import flask
from flask_httpauth import HTTPBasicAuth
import werkzeug  # noqa

from .config import parse as parse_config
from .config import Config  # noqa
from .errors import Error
from .pages import Pages, Page, PageNotFound, up_page
from .repository import Repository
from .helpers import cleanup_text


def create_auth(config: Config) -> HTTPBasicAuth:
    auth = HTTPBasicAuth()

    @auth.verify_password
    def verify_password(login: str, password: str) -> bool:
        if config.public_access:
            return True
        hashed_password = config.users.get(login)
        if not hashed_password:
            print("Unknow user:", login)
            return False
        try:
            nacl.pwhash.verify(hashed_password.encode(), password.encode())
            return True
        except nacl.exceptions.InvalidkeyError:
            print("Bad password for user:", login)
            return False

    return auth


def create_app(config: Optional[Config] = None) -> flask.Flask:  # noqa
    app = flask.Flask(__name__)
    app.jinja_env.undefined = jinja2.StrictUndefined

    if not config:
        config = parse_config()

    auth = create_auth(config)

    repo_path = config.repo_path
    try:
        git_repo = pygit2.Repository(repo_path)
    except pygit2.GitError as e:
        raise RepoNotFound(repo_path)

    if not git_repo.is_bare:
        raise NonBareRepo(repo_path)

    repository = Repository(git_repo)
    pages = Pages(repository)

    def redirect_to_page(name: str) -> Any:
        url = flask.url_for("view", name=name)
        return flask.redirect(url)

    @app.route("/")
    @auth.login_required
    def home() -> Any:
        return redirect_to_page("index")

    @app.route("/favicon.ico")
    @auth.login_required
    def favicon() -> Any:
        return flask.url_for("static", filename="favicon.ico")

    @app.route("/search")
    @auth.login_required
    def search() -> Any:
        pattern = flask.request.args.get("pattern")
        if not pattern:
            return flask.render_template("search_form.html")
        results = pages.search(pattern)
        return flask.render_template(
            "search_results.html", results=results, pattern=pattern
        )

    @app.route("/edit")
    @auth.login_required
    def edit() -> Any:
        name = flask.request.args["name"]
        page = pages.page(name)
        num_lines = len(page.markdown.splitlines())
        return flask.render_template("edit_form.html", page=page, num_lines=num_lines)

    @app.route("/save", methods=["POST"])
    @auth.login_required
    def save() -> Any:
        text = flask.request.form["text"]
        name = flask.request.form["name"]
        text = cleanup_text(text)
        pages.save(name, text)
        return redirect_to_page(name)

    @app.route("/add", methods=["GET", "POST"])
    @auth.login_required
    def add() -> Any:
        if flask.request.method == "GET":
            name = flask.request.args.get("name")
            return flask.render_template("add_form.html", name=name)
        else:
            name = flask.request.form["name"]
            title = flask.request.form["title"]
            if pages.exists(name):
                raise PageExists(name)
            text = "# " + title + "\n"
            pages.save(name, text)
            return redirect_to_page(name)

    @app.route("/view/<path:name>")
    @auth.login_required
    def view(name: str) -> Any:
        page = pages.page(name)
        return view_page(page)

    def view_page(page: Page) -> Any:
        parent = page.parent
        listing = pages.listing(parent=parent)
        up = up_page(parent)
        siblings = [pages.page(x) for x in listing.files[1:]]  # skip index
        children = [pages.page(x + "/index") for x in listing.dirs]
        return flask.render_template(
            "page.html", up=up, page=page, siblings=siblings, children=children
        )

    @app.route("/new")
    @auth.login_required
    def new_page() -> Any:
        name = flask.request.args["name"]
        blank_page = Page(name=name, markdown="")
        return flask.render_template("edit_form.html", page=blank_page, num_lines=10)

    @app.route("/rename/<path:old_name>", methods=["POST"])
    @auth.login_required
    def rename(old_name: str) -> Any:
        new_name = flask.request.form["new_name"]
        repository.rename(old_name + ".md", new_name + ".md")
        return redirect_to_page(new_name)

    @app.route("/remove/<path:name>", methods=["POST"])
    @auth.login_required
    def remove(name: str) -> Any:
        repository.remove(name + ".md")
        return redirect_to_page("index")

    @app.errorhandler(PageNotFound)
    def page_not_found(error: PageNotFound) -> Any:
        return flask.render_template("page_not_found.html", name=error.name), 404

    @app.errorhandler(PageExists)
    def page_exists(error: PageExists) -> Any:
        # TODO: flash?
        return flask.render_template("page_exists.html", name=error.name), 409

    return app


class PageExists(Error):
    def __init__(self, name: str):
        self.name = name


class RepoNotFound(Error):
    pass


class NonBareRepo(Error):
    pass
