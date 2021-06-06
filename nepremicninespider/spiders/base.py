# -*- coding: utf-8 -*-
from scrapy import Spider
from nepremicninespider.items import Nepremicnina
from nepremicninespider.secrets import mail_to as mail_default

class NepremicnineSpider(Spider):
    # This is a base class for spiders
    name = None
    mail_to = [mail_default]
    start_urls = None

    def parse(self, response):
        # Scrap multiple items per page
        ads = response.css('div.oglas_container')
        for item in ads:
            try:
                nepremicnina = Nepremicnina()
                nepremicnina['url'] = response.urljoin(item.css('a.slika::attr(href)').extract()[0])
                nepremicnina['iid'] = item.css('div::attr(id)').extract()[0]
                nepremicnina['title'] = item.css('h2 span::text').extract()[0]
                nepremicnina['desc'] = item.css('div.kratek::text').extract()[0]
                nepremicnina['price'] = item.css('span.cena::text').extract()[0]
                yield nepremicnina
            except Exception:
                pass

        # Next page
        for a in response.css('#pagination a.next'):
            yield response.follow(a, callback=self.parse)
