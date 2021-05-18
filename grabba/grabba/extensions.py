import collections
import logging

from twisted.internet import task

from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)

class CategoryStats:
    """Log category stats periodically"""

    def __init__(self, interval=60.0):
        self.stats = collections.defaultdict(int)
        self.detailed_stats = collections.defaultdict(int)
        self.interval = interval
        self.task = None

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('CATEGORY_STATS_ENABLED'):
            raise NotConfigured
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        if not interval:
            raise NotConfigured
        o = cls(interval)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        return o

    def spider_opened(self, spider):
        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def item_scraped(self, item, response, spider):
        key = item["gender"][0] if "gender" in item else "Unknown"
        key += "/" + (item["category"][0] if "category" in item else "None")
        self.stats[key] += 1
        key += "/" + (item["sub_category"][0] if "sub_category" in item else "None")
        key += "/" + (item["sub_sub_category"][0] if "sub_sub_category" in item else "None")
        self.detailed_stats[key] += 1

    def log(self, spider, detailed=False):
        msg = "Items scraped by Category "
        if detailed:
            msg += "(detailed): "
            stats = self.detailed_stats
        else:
            msg += "(summary): "
            stats = self.stats
        stats = sorted(stats.items())
        if len(stats) == 0:
            msg += "None!"
        else:
            msg += "\n - " + "\n - ".join(f"{k}: {v}" for k, v in stats) 
        logger.info(msg, extra={'spider': spider})

    def spider_closed(self, spider, reason):
        self.log(spider, detailed=True)
        if self.task and self.task.running:
            self.task.stop()

