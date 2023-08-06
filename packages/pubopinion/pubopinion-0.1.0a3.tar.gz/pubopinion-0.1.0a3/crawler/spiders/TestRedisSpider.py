from scrapy_redis.spiders import RedisSpider


class TestRedisSpider(RedisSpider):
    name = "TestRedisSpider"

    def start_requests(self):
        pass