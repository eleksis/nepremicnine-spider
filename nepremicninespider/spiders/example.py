# -*- coding: utf-8 -*-
from nepremicninespider.spiders.base import NepremicnineSpider
from nepremicninespider.items import Nepremicnina

class ParceleSpider(NepremicnineSpider):
    name = 'parcele-pomurje'
    start_urls = [
        'https://www.nepremicnine.net/oglasi-prodaja/pomurska/posest/zazidljiva/cena-do-20000-eur,velikost-do-1000-m2/'
        ]
