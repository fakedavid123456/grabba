# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ProductItem(Item):
    title = Field()
    price = Field()
    sale_price = Field()
    description = Field()
    brand = Field()
    category = Field()
    gender = Field()

