from urllib.parse import urljoin
import re
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def clear_value(value):
    return value.replace('\xa0', '')


def concat(string_list):
    return clear_value(''.join(string_list))



class HhVacancyLoader(ItemLoader):
    default_item_class = dict

    salary_in = concat
    description_in = concat
    # skills_in = MapCompose(skills_handler)

    name_out = TakeFirst()
    salary_out = TakeFirst()
    description_out = TakeFirst()
    # skills_out = TakeFirst()
    hh_url_out = TakeFirst()
    url_out = TakeFirst()


class HhEmployerLoader(ItemLoader):
    default_item_class = dict

    description_in = concat

    name_out = TakeFirst()
    url_out = TakeFirst()
    # fields_of_activity_out = TakeFirst()
    description_out = TakeFirst()
