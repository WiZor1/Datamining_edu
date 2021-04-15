# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GbParseItem(Item):
    title = Field()
    url = Field()
    description = Field()
    price = Field()
    author = Field()
    characteristics = Field()
