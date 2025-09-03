import dotenv
import requests
import scraper
import db
import os
from python_ntfy import NtfyClient


DB_PATH = "ebai.db"
QUERY = "https://www.kleinanzeigen.de/s-fahrraeder/damen,herren/boeblingen/anzeige:angebote/preis::0/fahrrad/k0c217l8782r20+fahrraeder.art_s:(damen%2Cherren)+fahrraeder.type_s:(city%2Cmountainbike)"


def main():
    dotenv.load_dotenv()

    require_env("NTFY_USER")
    require_env("NTFY_PASS")
    require_env("NTFY_SERVER")
    require_env("NTFY_TOPIC")

    db.setup_db(DB_PATH)

    scraped = scraper.scrape_articles(requests.get(QUERY).content)
    scraped_ids = [id for (id, _) in scraped]
    stored_ids = [id for (id, _) in db.get_ads()]

    new_article_count = 0
    for scraped_id in scraped_ids:
        if scraped_id not in stored_ids:
            print(f"new article: {scraped_id}")
            new_article_count += 1

    db.clear()
    for (id, name) in scraped:
        db.insert_ad(id, name)

    print(f"{new_article_count} new article(s)")
    if new_article_count > 0:
        c = NtfyClient(server=os.getenv("NTFY_SERVER"), topic=os.getenv("NTFY_TOPIC"), auth=(os.getenv("NTFY_USER"), os.getenv("NTFY_PASS")))
        c.send(f"{new_article_count} neue{('r' if new_article_count == 1 else '')} Artikel")


def require_env(envvar):
    if os.getenv(envvar) is None:
        raise RuntimeError(f"Missing required environment variable: {envvar}")


if __name__ == "__main__":
    main()
