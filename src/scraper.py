from bs4 import BeautifulSoup as bs


def scrape_articles(content: str) -> [(int, str)]:
    soup = bs(content, 'html.parser')
    articles = soup.select("article.aditem")

    res = [
        (
            article.attrs["data-adid"],
            article.select("a.ellipsis")[0].contents[0],
        )
        for article in articles
    ]

    return res
