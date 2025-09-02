import dotenv
import os
import requests
import sqlite3


API = "https://api.kleinanzeigen-agent.de/ads/v1/kleinanzeigen"
DB_PATH = "ebai.db"


QUERY = "Fahrrad"
LOCATION = "Böblingen"
RADIUS = 10


def main():
    dotenv.load_dotenv()

    setup_db()

    location_id = get_location(LOCATION)
    print(f"got Location ID {location_id} for {LOCATION}")

    ads = search_ads(QUERY, location_id=location_id, radius=RADIUS, limit=10)
    print(ads.json())


def get_api_key():
    return os.getenv("API_KEY")


def api_get(endpoint, params):
    print(f"fetching {endpoint} with {params}")
    return requests.get(API + endpoint, params, headers={
        "ads_key": get_api_key(),
        "Content-Type": "application/json"
    })


def setup_db():
    db_exists = os.path.exists(DB_PATH)
    global db
    global db_cursor
    db = sqlite3.connect(DB_PATH)
    db_cursor = db.cursor()
    if not db_exists:
        db_cursor.execute("CREATE TABLE locations (name, id)")


def get_location(location):
    res = db_cursor.execute(f"SELECT id FROM locations WHERE name='{location}'").fetchone()

    if res is None:
        response = api_get("/locations", params={
            "query": location,
            "limit": 1
        })

        loc_id = response.json()["data"]["locations"][0]["id"]
        db_cursor.execute(f"INSERT INTO locations VALUES ('{location}', {loc_id})")
        db.commit()

        return loc_id

    return res[0]


def search_ads(query, location):
    params = {
        "query": query,
        "limit": limit,
        "sort": "cheapest",
        "max_price": 0
    }
    if location_id is not None:
        params["location_id"] = location_id
        if radius is not None:
            params["radius"] = radius

    return api_get(endpoint="/search", params=params)


if __name__ == "__main__":
    main()
