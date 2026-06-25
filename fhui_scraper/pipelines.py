import logging

import scrapy
from scrapy.pipelines.files import FilesPipeline, FileException
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)


class PdfDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item) if item else None
        vol = adapter.get("volume", "unknown") if adapter else "unknown"
        iss = adapter.get("issue", "unknown") if adapter else "unknown"
        aid = adapter.get("article_id", "unknown") if adapter else "unknown"
        return f"{vol}_{iss}/{aid}.pdf"

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        pdf_url = adapter.get("pdf_url")
        if pdf_url:
            yield scrapy.Request(pdf_url)

    def media_downloaded(self, response, request, info, *, item=None):
        if response.status not in (200, 202):
            logger.warning(f"PDF download returned status {response.status} for {request.url}")
            raise FileException("download-error")
        return super().media_downloaded(response, request, info, item=item)

    def item_completed(self, results, item, info):
        adapter = ItemAdapter(item)
        for ok, result in results:
            if ok:
                adapter["pdf_path"] = result.get("path")
                break
        return item


class DuplicateFilterPipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        key = adapter.get("doi") or adapter.get("article_url")
        if key in self.seen:
            raise scrapy.exceptions.DropItem(f"Duplicate: {key}")
        self.seen.add(key)
        return item
