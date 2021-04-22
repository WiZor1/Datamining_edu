import scrapy
from scrapy.http import Request
# import scrapy.spidermiddlewares.httperror
from Lesson6.avito_parse.loaders import AvitoLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['www.avito.ru']
    start_urls = ['https://www.avito.ru/krasnodar/nedvizhimost/']
    # handle_httpstatus_list = [429]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          cookies={'currency': 'USD', 'country': 'UY'},
                          callback=self.parse
                          )

    @staticmethod
    def _get_follow_xpath(response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, **kwargs)

    def parse(self, response, **kwargs):
        if 'nedvizhimost' in response.url:
            yield from self._get_follow_xpath(
                response, self._xpath_selectors['start_url'], callback=self.parse
            )
        else:
            print(1)
            yield from self._get_follow_xpath(
                response, self._xpath_selectors['pagination'], callback=self.parse
            )
            yield from self._get_follow_xpath(
                response, self._xpath_selectors['flat'], callback=self.parse_flat
            )

    def parse_flat(self, response):
        print(1)
        loader = AvitoLoader(response=response)
        loader.add_value('avito_url', response.url)
        for key, selector in self._xpath_data_query.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()
        pass

    _xpath_selectors = {
        'start_url': '//ul[@data-marker="rubricator/list"]//a[@title="Все квартиры"]/@href',
        'pagination': '//div[@class="pagination-pages clearfix"]/a/@href',
        'flat': '//div[@data-marker="catalog-serp"]//div[contains(@class, "iva-item-content")]//a/@href'
    }

    _xpath_data_query = {
        'url': 'url',
        'title': '//span[@class="title-info-title-text"]/text()',
        'price': '//div[@class="item-price-wrapper"]//span[@class="js-item-price"]/@content',
        'address': '//div[@class="item-map-location"]//div[@itemprop="address"]//text()',
        'characteristics': '//div[@class="item-view-content-left"]'
                           '//ul[@class="item-params-list"]/li[@class="item-params-list-item"]//text()',
        'author_url': '//div[contains(@class, "item-view-seller-info")]'
                      '//div[@class="seller-info-value"]/div[@data-marker="seller-info/name"]/a/@href',
        # 'phone': '',
    }
