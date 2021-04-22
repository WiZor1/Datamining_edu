from urllib.parse import urljoin
import re
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class AvitoLoader(ItemLoader):
    default_item_class = dict

    url_out = TakeFirst()
    title_out = TakeFirst()
    price_out = TakeFirst()
    address_out = TakeFirst()
    characteristics_out = TakeFirst()
    author_url_out = TakeFirst()
