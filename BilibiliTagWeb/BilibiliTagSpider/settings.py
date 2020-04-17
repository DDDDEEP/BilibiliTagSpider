# -*- coding: utf-8 -*-

# Scrapy settings for BilibiliTagSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BilibiliTagSpider'

SPIDER_MODULES = ['BilibiliTagSpider.spiders']
NEWSPIDER_MODULE = 'BilibiliTagSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'BilibiliTagSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 4
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Host': 'api.bilibili.com',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'BilibiliTagSpider.middlewares.BilibilitagspiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'BilibiliTagSpider.middlewares.BilibilitagspiderDownloaderMiddleware': 543,
    'BilibiliTagSpider.middlewares.RandomUserAgentMiddlware': 543,
    # 'BilibiliTagSpider.middlewares.ProxyMiddleware': 555,
}
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
MYEXT_ENABLED = True
EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': None,
    # 'BilibiliTagSpider.extensions.DumpStatsExtension': 100,
    'BilibiliTagSpider.extensions.SpiderProgressLogging': 500,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300, # 分布式
    'BilibiliTagSpider.pipelines.BilibilitagspiderPipeline': 300,
    'BilibiliTagSpider.pipelines.MongoPipeline': 350,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 数据库
MONGO_URI = 'localhost'
MONGO_DB = 'bilibili_tag'
MONGO_USR = 'root'
MONGO_PWD = 'root'

# 爬虫相关变量
PER_PAGE = 100  # 列表api的分页量

# 日志设置
LOG_LEVEL = 'INFO'
LOG_STDOUT = True  # 使用Scrapyd时需要关闭该选项

# 本地获取代理的地址
PROXY_URL = '127.0.0.1:5555/random'

# 随机用户代理的类型
RANDOM_UA_TYPE = 'chrome'

# Scrapy-Redis分布式设置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
FEED_EXPORT_ENCODING = 'utf-8'
REDIS_HOST = '127.0.0.1'
REDIS_PARAMS = {
    'password': 'root',
}
REDIS_PORT = 6379
