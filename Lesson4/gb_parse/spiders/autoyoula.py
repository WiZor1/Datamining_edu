import scrapy
import re

class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]
    _css_selectors = {
        "brands": "div.ColumnItemList_container__5gTrc a.blackLink",
        "pagination": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "car": "#serp article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu",
    }

    def _get_follow(self, response, selector_css, callback, **kwargs):
        for link_selector in response.css(selector_css):
            yield response.follow(link_selector.attrib.get("href"), callback=callback)

    def parse(self, response, **kwargs):
        yield from self._get_follow(response, self._css_selectors["brands"], self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_follow(response, self._css_selectors["pagination"], self.brand_parse)
        yield from self._get_follow(response, self._css_selectors["car"], self.car_parse)

    def car_parse(self, response):
        data = {
            "title": response.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "url": response.url,
            "description": response.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first(),
            "price": self.clear_price(response.css("div.AdvertCard_price__3dDCr::text")),
            "characteristics": [
                {
                    "name": itm.css(".AdvertSpecs_label__2JHnS::text").extract_first(),
                    "value": itm.css(".AdvertSpecs_data__xK2Qx::text").extract_first()
                             or itm.css(".AdvertSpecs_data__xK2Qx a::text").extract_first(),
                }
                for itm in response.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")
            ],
            "author": self.get_author_id(response),
        }
        yield data

    def get_author_id(self, resp):
        marker = "window.transitState = decodeURIComponent"
        for script in resp.css("script"):
            try:
                if marker in script.css("::text").extract_first():
                    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                    result = re.findall(re_pattern, script.css("::text").extract_first())
                    return (
                        resp.urljoin(f"/user/{result[0]}").replace("auto.", "", 1)
                        if result
                        else None
                    )
            except TypeError:
                pass

    @staticmethod
    def clear_price(price):
        try:
            result = float(price.get().replace("\u2009", ""))
        except ValueError:
            result = None
        return result