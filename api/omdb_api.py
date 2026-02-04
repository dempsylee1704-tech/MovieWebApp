import requests
import os
from dotenv import load_dotenv
load_dotenv()



BASE_URL = "https://www.omdbapi.com/"
apikey = os.getenv("OMDB_API_KEY")

if not apikey:
    raise RuntimeError("OMDB_API_KEY not found")

def get_request_from_api(movie_title):
    try:
        res = requests.get(BASE_URL, params={
            "apikey": apikey,
            "t": movie_title
        })
        data = res.json()

        if data.get("Response") == "False":
            return None

        year_raw = data.get("Year", "")
        year = int(year_raw[:4]) if year_raw[:4].isdigit() else None

        return {
            "title": data.get("Title"),
            "year": year,
            "director": data.get("Director"),
            "poster": data.get("Poster")
        }

    except Exception:
        return None



if __name__ == "__main__":
    print(get_request_from_api("Titanic"))