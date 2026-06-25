import re
import scrapy
from fhui_scraper.items import ArticleItem


class FacultyLawSpider(scrapy.Spider):
    name = "faculty_law"
    allowed_domains = ["scholarhub.ui.ac.id"]

    def __init__(self, journal_codes=None, max_articles=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_articles = int(max_articles) if max_articles else None
        self.journal_map = {}
        if journal_codes:
            codes = [c.strip() for c in journal_codes.split(",")]
            self.start_urls = [
                f"https://scholarhub.ui.ac.id/{code}/all_issues.html"
                for code in codes
            ]
            for code in codes:
                self.journal_map[code] = {
                    "code": code,
                    "name": None,
                    "url": f"https://scholarhub.ui.ac.id/{code}",
                }
        else:
            self.start_urls = ["https://scholarhub.ui.ac.id/law/"]

    def parse(self, response):
        if "law" in response.url and self.journal_map == {}:
            for link in response.css("#series-home p a"):
                url = link.attrib.get("href")
                code = url.rstrip("/").split("/")[-1]
                name = link.css("::text").get()
                self.journal_map[code] = {"code": code, "name": name, "url": url}
                yield response.follow(
                    url.rstrip("/") + "/all_issues.html",
                    callback=self.parse_journal,
                    meta={"journal_code": code},
                )
        else:
            journal_code = self._code_from_url(response.url)
            yield from self.parse_journal(response)

    def parse_journal(self, response):
        journal_code = response.meta.get("journal_code") or self._code_from_url(response.url)
        info = self.journal_map.get(journal_code, {})
        journal_name = info.get("name")
        journal_url = info.get("url") or f"https://scholarhub.ui.ac.id/{journal_code}"

        for issue_link in response.css("div.item h3.issue a"):
            yield response.follow(
                issue_link,
                callback=self.parse_issue,
                meta={
                    "journal_code": journal_code,
                    "journal_name": journal_name,
                    "journal_url": journal_url,
                },
            )

    def parse_issue(self, response):
        issue_url = response.url.rstrip("/") + "/"
        links = response.css("div.doc p a[href*='/vol']")
        if self.max_articles:
            links = links[: self.max_articles]
        for article_link in links:
            yield response.follow(
                article_link,
                callback=self.parse_article,
                meta={**response.meta, "issue_url": issue_url},
            )

    def parse_article(self, response):
        item = ArticleItem()
        item["article_url"] = response.url
        item["issue_url"] = response.meta["issue_url"]
        item["journal_code"] = response.meta["journal_code"]
        item["journal_url"] = response.meta.get("journal_url")
        item["journal"] = (
            self._meta(response, "bepress_citation_journal_title")
            or response.meta.get("journal_name")
        )
        item["title"] = self._meta(response, "bepress_citation_title")
        item["volume"] = self._meta(response, "bepress_citation_volume")
        item["issue"] = self._meta(response, "bepress_citation_issue")
        item["year"] = self._meta(response, "bepress_citation_date")
        item["doi"] = self._meta(response, "bepress_citation_doi")
        item["first_page"] = self._meta(response, "bepress_citation_firstpage")
        item["issn"] = self._meta(response, "bepress_citation_issn")
        item["online_date"] = self._meta(response, "bepress_citation_online_date")
        item["abstract"] = self._meta(response, "description")
        item["keywords"] = self._meta(response, "keywords")
        item["pdf_url"] = self._meta(response, "bepress_citation_pdf_url")
        item["authors"] = self._metas(response, "bepress_citation_author")
        item["institutions"] = self._metas(response, "bepress_citation_author_institution")

        m = re.search(r"/vol(\d+)/iss(\d+)/(\d+)", response.url)
        if m:
            item["article_id"] = m.group(3)

        yield item

    def _code_from_url(self, url):
        m = re.search(r"scholarhub\.ui\.ac\.id/(\w+)/", url)
        return m.group(1) if m else "unknown"

    def _meta(self, response, name):
        el = response.css(f'meta[name="{name}"]')
        if el:
            return el.attrib.get("content")

    def _metas(self, response, name):
        return [
            el.attrib.get("content")
            for el in response.css(f'meta[name="{name}"]')
        ]
