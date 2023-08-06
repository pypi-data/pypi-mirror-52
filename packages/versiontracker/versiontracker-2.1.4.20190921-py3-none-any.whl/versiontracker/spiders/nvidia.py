from scrapy import Request

from ..items import Item

from . import Spider


class NVidia(Spider):
    name = 'nvidia'

    def first_request(self, data):
        return 'http://www.nvidia.com/object/unix.html'

    def parse(self, response):
        pattern = r'(?i)latest\s+short\s+lived\s+branch\s+version\s*:'
        xpath = '//text()[re:test(., "{}")]/following-sibling::a/@href'.format(
            pattern)
        return Request(
            response.xpath(xpath).extract_first(),
            callback=self.parse_details,
            meta=response.meta)

    @staticmethod
    def parse_details(response):
        date = response.xpath(
            '//td[@id=\'tdReleaseDate\']/text()').extract_first()
        version = response.xpath(
            '//td[@id=\'tdVersion\']/text()').extract_first().strip()
        return Item(date=date, response=response, version=version)
