import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    institutions = scrapy.Field()
    volume = scrapy.Field()
    issue = scrapy.Field()
    year = scrapy.Field()
    doi = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()
    first_page = scrapy.Field()
    pdf_url = scrapy.Field()
    article_url = scrapy.Field()
    journal = scrapy.Field()
    journal_code = scrapy.Field()
    journal_url = scrapy.Field()
    issn = scrapy.Field()
    online_date = scrapy.Field()
    article_id = scrapy.Field()
    issue_url = scrapy.Field()
