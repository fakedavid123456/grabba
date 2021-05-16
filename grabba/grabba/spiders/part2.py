import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose

from grabba.items import ProductItem

import yaml


class Part2Spider(CrawlSpider):
    name = 'part2'
    
    def __init__(self, config):
        with open(config) as f:
            self.config = yaml.safe_load(f.read())

        self.allowed_domains = self.config["allowed_domains"]
        self.rules = (
            Rule(LinkExtractor(allow=self.config["index_pages"])),
            Rule(LinkExtractor(allow=self.config["detail_pages"]), callback='parse_item')
        )
        super().__init__()

    def start_requests(self):
        yield Request("https://theurge.com/women/search/?cat=clothing-dresses")

    def parse_item(self, response):
        item = scrapy.Item()
        l = ItemLoader(item=item, response=response)
        '''
        l.add_css("title", "span._3mRKt::text", Join(), MapCompose(str.strip))
        l.add_css("sale_price", "div.eP0wn._26-lJ._28iFq::text", Join(), MapCompose(str.strip), re='[,.0-9]+')
        l.add_css("full_price", "span._2plVT._35rbh::text", re="[,.0-9]+")
        l.add_css("description", "div._34YUR._1K7NF > span::text", MapCompose(str.strip))
        l.add_css("brand", "h1._1psEi > a::text")
        l.add_css("category", "li._1Hb_0:nth-child(4) > a > span::text")
        '''
        for a in self.config["attributes"]:
            item.fields[a["name"]] = scrapy.Field()
            
            processors = []
            if "processors" in a:
                for p in a["processors"]:
                    if p == "join":
                        processors.append(Join())
                    elif p == "strip":
                        processors.append(MapCompose(str.strip))

            kwargs = {}
            if "regex" in a:
                kwargs["re"] = a["regex"]

            l.add_css(a["name"], a["selector"], *processors, **kwargs)
        
        item.fields["url"] = scrapy.Field()
        l.add_value("url", response.url)

        return l.load_item()

