# -*- coding: utf-8 -*-
BOT_NAME = ['tweetsSpider', 'informationSpider']

SPIDER_MODULES = ['Sina_spider2.spiders']
NEWSPIDER_MODULE = 'Sina_spider2.spiders'

DOWNLOADER_MIDDLEWARES = {
    "Sina_spider2.middleware.UserAgentMiddleware": 401,
    "Sina_spider2.middleware.CookiesMiddleware": 402,
}
ITEM_PIPELINES = ["Sina_spider2.pipelines.ScrapyWeiboPipeline"]

SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIE_URL = None
REDIS_HOST = '10.24.148.239'
REDIS_PORT = 6379

DOWNLOAD_DELAY = 2  # 间隔时间
COMMANDS_MODULE = 'Sina_spider2.commands'
# LOG_LEVEL = 'INFO'  # 日志级别
# CONCURRENT_REQUESTS = 1
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1


MYSQL_HOST = "rdsrz83899gt40q8fm5p.mysql.rds.aliyuncs.com"
USER_NAME = "sina"
PASSWORD = "qwer1234"
DATABASE = "sina"
