import json

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.item import Item, Field

from grabba.items import ProductItem


class Part1Spider(scrapy.Spider):
    name = 'part1'
    allowed_domains = ['api.theurge.com']

    def start_requests(self):
        for i in range(1, 16):
            url = f"https://api.theurge.com.au/search-results?page={i}&currency=AUD&cat=clothing-tops&gender=female&language=en&country=au&client=theurge"
            request = Request(url)
            yield request


    def parse(self, response):
        data = json.loads(response.text)["data"]
        for d in data:
            item = ProductItem()
            l = ItemLoader(item=item, response=response)
            l.add_value("title", d["attributes"]["product_name"])
            l.add_value("price", d["attributes"]["retailer_price"])
            if "sale_price" in d["attributes"]:
                l.add_value("sale_price", d["attributes"]["sale_price"])
            l.add_value("description", d["attributes"]["long_description"])
            l.add_value("brand", d["attributes"]["e_brand_formatted"])
            l.add_value("category", d["attributes"]["e_cat_l2"][0])
            if "gender" in d["attributes"]:
                l.add_value("gender", d["attributes"]["gender"])

            yield l.load_item()

