import pytest
from zpov.repository import Repository
from zpov.pages import Pages, parent_page, up_page, PageNotFound


def test_simple_page(repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n\nThis is the index\n")
    pages = Pages(repository)
    assert pages.total() == 1
    index_md = pages.markdown("index")
    assert "This is the index" in index_md

    index_page = pages.page("index")

    assert index_page.name == "index"
    assert index_page.title == "Welcome"
    index_html = index_page.html
    assert "<h1>Welcome" in index_html


def test_search(repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n\nindex matches foo\n")
    repository.write_file("bar/foo.md", "# Bar\n\nbar/foo also matches foo\n")
    repository.write_file("bar/index.md", "# Bar Index\n\nbar does not match\n")
    pages = Pages(repository)
    actual = pages.search("foo")
    assert len(actual) == 2
    actual_names = [x.name for x in actual]
    assert actual_names == ["bar/foo", "index"]


@pytest.fixture
def repo_with_tree(repository: Repository) -> Repository:
    repository.write_file("index.md", "# Welcome\n")
    repository.write_file("a_file.md", "# A file\n")
    repository.write_file("foo/bar.md", "# Bar \n")
    repository.write_file("foo/index.md", "# Foo\n")
    repository.write_file("spam/index.md", "# Spam\n")
    repository.write_file("spam/01_one.md", "# One\n")
    repository.write_file("spam/02_two.md", "# Two\n")
    repository.write_file("spam/sub/three.md", "# Three\n")
    repository.write_file("spam/sub/deep/foo", "# Four\n")
    return repository


def test_listing_top(repo_with_tree: Repository) -> None:
    pages = Pages(repo_with_tree)
    actual = pages.listing(parent="")
    assert actual.dirs == ["foo", "spam"]
    assert actual.files == ["index", "a_file"]


def test_get_listing_sub_dir(repo_with_tree: Repository) -> None:
    pages = Pages(repo_with_tree)
    actual = pages.listing(parent="spam")
    assert actual.dirs == ["spam/sub"]
    assert actual.files == ["spam/index", "spam/01_one", "spam/02_two"]


def test_page_not_found(repo_with_tree: Repository) -> None:
    pages = Pages(repo_with_tree)
    with pytest.raises(PageNotFound):
        pages.page("no-such")


def test_exists(repo_with_tree: Repository) -> None:
    pages = Pages(repo_with_tree)
    assert pages.exists("index")
    assert not pages.exists("no-such")


def test_parent_page() -> None:
    assert parent_page("spam") == ""
    assert parent_page("spam/foo") == "spam"
    assert parent_page("spam/foo/bar") == "spam/foo"


def test_up_page() -> None:
    assert up_page("") is None
    assert up_page("spam") == "index"
    assert up_page("spam/foo") == "spam/index"
    assert up_page("spam/foo/bar") == "spam/foo/index"
