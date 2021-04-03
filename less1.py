import requests
import json
from pathlib import Path

api_url = "https://5ka.ru/api/v2/special_offers/"

headers = {
    "User-Agent": "OH MY"
}

params = {
    "categories": 940,
    "ordering": None,
    "page": 1,
    "price_promo__gte": None,
    "price_promo__lte": None,
    "records_per_page": 20,
    "search": None,
    "store": None
}

response = requests.get(api_url, headers=headers, params=params)

print(1)

file = Path(__file__).parent.joinpath('res.json')

file.write_text(response.text, encoding='utf-8')

data = json.loads(response.text)

print(len(data["results"]))

cat_url = "https://5ka.ru/api/v2/categories/"

cat_resp = requests.get(cat_url, headers=headers)
data = cat_resp.json()

cat_file = Path(__file__).parent.joinpath('res_for_cat.json')
cat_file.write_text(cat_resp.text, encoding="utf-8")

