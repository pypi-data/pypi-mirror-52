from typing import Any
from zpov.repository import Repository

# FIXME
TestClient = Any


def test_home(client: TestClient, repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n")
    response = client.get("/")
    assert response.status_code == 302
    redirect_url = response.headers["location"]
    response = client.get(redirect_url)
    assert response.status_code == 200


def test_view_index(client: TestClient, repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n")
    response = client.get("/view/index")
    assert response.status_code == 200


def test_edit_form(client: TestClient, repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n")
    response = client.get("/edit?name=index")
    assert response.status_code == 200
    html = response.data.decode()
    assert "form" in html
    assert "textarea" in html


def test_save_page(client: TestClient, repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n")
    response = client.post(
        "/save?name=index",
        data={"text": "# Welcome\nThis has been added", "name": "index"},
    )
    response = client.get("/view/index")
    assert response.status_code == 200
    html = response.data.decode()
    assert "This has been added" in html


def test_add_form(client: TestClient, repository: Repository) -> None:
    response = client.get("/add?name=index")
    assert response.status_code == 200
    html = response.data.decode()
    assert "form" in html
    assert 'action="/add"' in html


def test_add_page(client: TestClient, repository: Repository) -> None:
    response = client.post("/add", data={"name": "index", "title": "Welcome"})
    assert response.status_code == 302
    redirect_url = response.headers["location"]
    response = client.get(redirect_url)
    assert response.status_code == 200


def test_view_in_subdir(client: TestClient, repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n")
    repository.write_file("one/foo.md", "# Foo\n")
    response = client.get("/view/one/foo")
    assert response.status_code == 200


def test_search(client: TestClient, repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n")
    repository.write_file("foo/bar.md", "# Bar\nMentions foo")
    repository.write_file("foo/baz.md", "# Baz\nAlso mentions foo")
    response = client.get("/search")
    assert response.status_code == 200
    html = response.data.decode()
    assert "form" in html
    assert 'action="/search"' in html

    response = client.get("/search?pattern=foo")
    assert response.status_code == 200
    html = response.data.decode()
    assert 'href="/view/foo/bar"' in html


def test_add_conflict(client: TestClient, repository: Repository) -> None:
    repository.write_file("index.md", "# Welcome\n")
    response = client.post("/add", data={"name": "index", "title": "Welcome"})
    assert response.status_code == 409
