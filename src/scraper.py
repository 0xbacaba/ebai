from bs4 import BeautifulSoup as bs
import requests
import db
import ntfy
from exceptions import EbaiException


def scrape_articles(query: str) -> [(int, str)]:
    try:
        res = requests.get(query)
    except ConnectionError as e:
        err_id = EbaiException.RequestException
        if not db.has_error(err_id):
            db.insert_error(err_id, e.strerror)
            ntfy.send_err(err_id, e.strerror)
        return None

    if res.status_code != 200:
        err_id = EbaiException.RequestException
        if not db.has_error(err_id):
            err_text = f"Unexpected status code: {res.status_code}"
            db.insert_error(err_id, err_text)
            ntfy.send_err(err_id, err_text)

        return None

    db.remove_error(EbaiException.RequestException)

    soup = bs(res.content, 'html.parser')
    articles = soup.select("article.aditem")

    res = [
        (
            article.attrs["data-adid"],
            article.select("a.ellipsis")[0].contents[0],
        )
        for article in articles
    ]

    return res
