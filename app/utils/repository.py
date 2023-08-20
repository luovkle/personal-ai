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
