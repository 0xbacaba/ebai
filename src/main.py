import scraper
import db
import ntfy
import dotenv
import os
import sys
from time import sleep


DB_PATH = "data/ebai.db"
QUERY = "https://www.kleinanzeigen.de/s-fahrraeder/damen,herren/boeblingen/anzeige:angebote/preis::0/fahrrad/k0c217l8782r20+fahrraeder.art_s:(damen%2Cherren)+fahrraeder.type_s:(city%2Cmountainbike)"


def main():
    dotenv.load_dotenv()

    require_env("NTFY_USER")
    require_env("NTFY_PASS")
    require_env("NTFY_SERVER")
    require_env("NTFY_TOPIC")

    db.setup_db(DB_PATH)
    ntfy.init()

    delay = 60
    if len(sys.argv) == 2:
        delay = float(sys.argv[1])

    while True:
        run()
        if delay == 0:
            break
        sleep(delay)


def run():
    scraped = scraper.scrape_articles(QUERY)
    if scraped is None:
        return
    stored_ids = [id for (id, _) in db.get_ads()]

    new_articles = []
    for (scraped_id, scraped_name) in scraped:
        if scraped_id not in stored_ids:
            print(f"new article: {scraped_id}")
            new_articles.append((scraped_id, scraped_name))

    db.clear()
    for (id, name) in scraped:
        db.insert_ad(id, name)

    new_article_count = len(new_articles)
    print(f"{new_article_count} new article(s)")
    if new_article_count > 0:
        new_names = '\n'.join(name for (_, name) in new_articles)
        ntfy.send(f"{new_article_count} neue{('r' if new_article_count == 1 else '')} Artikel", new_names)


def require_env(envvar):
    if os.getenv(envvar) is None:
        raise RuntimeError(f"Missing required environment variable: {envvar}")


if __name__ == "__main__":
    main()
