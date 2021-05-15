import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose

from grabba.items import ProductItem


class Part1Spider(CrawlSpider):
    name = 'part1'
    allowed_domains = ['theurge.com']
    start_urls = ['https://theurge.com/women/search/?cat=clothing-dresses']

    rules = (
        Rule(LinkExtractor(allow='/women/search/')),
        Rule(LinkExtractor(allow='/product/'), callback='parse_item')
    )

    def parse_item(self, response):
        item = ProductItem()

        l = ItemLoader(item=item, response=response)
        l.add_css("title", "span._3mRKt::text", Join(), MapCompose(str.strip))
        l.add_css("sale_price", "div.eP0wn._26-lJ._28iFq::text", Join(), MapCompose(str.strip), re='[,.0-9]+')
        l.add_css("full_price", "span._2plVT._35rbh::text", re="[,.0-9]+")
        l.add_css("description", "div._34YUR._1K7NF > span::text", MapCompose(str.strip))
        l.add_css("brand", "h1._1psEi > a::text")
        l.add_css("category", "li._1Hb_0:nth-child(4) > a > span::text")

        l.add_value("url", response.url)

        return l.load_item()
