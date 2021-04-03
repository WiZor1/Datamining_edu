import requests
from pathlib import Path
import json
import time


class Parse5ka:
    headers = {
        "User-Agent": "OH MY"
    }
    params = {
        "records_per_page": 20,
    }

    def __init__(self, api_url, path: Path):
        self.api_url = api_url
        self.path = path

    def _get_response(self, api_url):
        response = requests.get(api_url, headers=self.headers, params=self.params)
        if response.status_code in [200, 301, 302]:
            return response
        time.sleep(0.5)

    def run(self):
        for product in self._parse(self.api_url):
            product_path = self.path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url: str):
        while url:
            data = self._get_response(url).json()
            url = data["next"]
            for product in data["results"]:
                yield product

    @staticmethod
    def _save(data, path):
        path.write_text(json.dumps(data), encoding='utf-8')


class CategoryParse5ka(Parse5ka):
    def __init__(self, api_url, category_url, path: Path, maximize_page_size='records_per_page=20'):
        self.category_url = category_url
        self.maximize_page_size = maximize_page_size
        super().__init__(api_url, path)

    def run(self):
        for category in self._get_categories():
            cat_url = f"{self.api_url}?categories={category['parent_group_code']}&{self.maximize_page_size}"

            products = list(self._parse(cat_url))
            file_name = f"{category['parent_group_code']}_{category['parent_group_name']}.json"
            category_path = self.path.joinpath(file_name)
            category_dict = {
                "name": category['parent_group_name'],
                "code": category['parent_group_code'],
                "products": products
            }
            self._save(category_dict, category_path)

    def _get_categories(self):
        cat_resp = self._get_response(self.category_url)
        categories = cat_resp.json()
        return categories


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    # product_save_path = get_save_path("products")
    categories_save_path = get_save_path("categories")
    # prod_parser = Parse5ka(url, categories_save_path)
    cat_parser = CategoryParse5ka(url, cat_url, categories_save_path)
    # prod_parser.run()
    cat_parser.run()
