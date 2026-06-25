BOT_NAME = "fhui_scraper"

SPIDER_MODULES = ["fhui_scraper.spiders"]
NEWSPIDER_MODULE = "fhui_scraper.spiders"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 16
DOWNLOAD_DELAY = 0.25

ITEM_PIPELINES = {
    "fhui_scraper.pipelines.DuplicateFilterPipeline": 100,
}

FEEDS = {
    "articles.json": {
        "format": "jsonlines",
        "encoding": "utf-8",
        "fields": [
            "title", "authors", "institutions", "volume", "issue", "year",
            "doi", "abstract", "keywords", "first_page", "pdf_url",
            "article_url", "journal", "journal_code", "journal_url",
            "issn", "online_date", "article_id", "issue_url",
        ],
    },
}

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [301, 403]

FEED_EXPORT_ENCODING = "utf-8"
