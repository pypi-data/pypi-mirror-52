from .xpath import XPath


class PyPI(XPath):
    name = 'pypi'

    def first_request(self, data):
        data['package'] = data.get('package', data['id'])
        return "https://pypi.org/project/{}/".format(data['package'])

    def parse(self, response):
        meta = response.meta
        meta.update(XPath.params)
        meta['base'] = '//div[contains(@class, \'release--current\')]'
        meta['version'] = \
            '//p[contains(@class, \'release__version\')]//text()'
        meta['date'] = '//time/@datetime'
        meta['url-xpath'] = \
            '//p[contains(@class, \'release__version\')]/ancestor::a[1]/@href'
        return super().parse(response)
