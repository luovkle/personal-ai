import json
from pathlib import Path
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_repo_data(url: str) -> dict:
    repo = {
        "url": url,
        "name": "",
        "description": "",
        "langs": [],
    }

    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "lxml")

    # name
    a = soup.find(
        "a",
        attrs={
            "data-pjax": "#repo-content-pjax-container",
            "data-turbo-frame": "repo-content-turbo-frame",
        },
    )
    repo["name"] = a.text.strip() if a else ""

    # description
    p = soup.find("p", attrs={"class": "f4 my-3"})
    repo["description"] = p.text.strip() if p else ""

    # langs
    a_list = soup.find_all(
        "a",
        attrs={
            "class": "d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3"
        },
    )
    for a in a_list:
        lang, percent = [span.text.strip() for span in a.find_all("span")]
        repo["langs"].append({"lang": lang, "percent": percent})

    return repo


def get_projects(urls: list[str]):
    data_path = Path.cwd() / "app" / "data"
    repos_path = data_path / "repos.json"
    if not repos_path.is_file():
        if not data_path.is_dir():
            data_path.mkdir()
        repos = [get_repo_data(repo) for repo in urls]
        with open(repos_path, "w") as f:
            json.dump(repos, f)
        return repos
    with open(repos_path) as f:
        return json.load(f)
