# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.mail import MailSender
from nepremicninespider.secrets import mail_server, mail_port, mail_username, mail_password
from nepremicninespider.items import Nepremicnina
from datetime import date
import os


class NepremicninespiderPipeline(object):

    def open_spider(self, spider):
        self.known_items = dict()
        self.new_items = dict() # Need this to send them via mail
        self.db_path = 'db/' + spider.name + '.txt'
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    scraped, iid, price, title, desc, url = line.split('|')
                    self.known_items[iid] = { 'date': scraped, 'iid': iid, 'price': price, 'title': title, 'desc': desc, 'url': url }

    def process_item(self, item, spider):
        # Sometimes we get item that is out of our filters (weird ads)
        # .seznam [class*="ogIasi"], .seznam [class*="oġlasi"], .seznam [class*="oglas¡"], .seznam [class*="oglàsi"], .seznam [class*="oglási"], .seznam [class*="oglasì"], .seznam [class*="ąds"], .seznam [class*="àds"], .seznam [class*="áds"], .seznam [class*="äds"], .seznam [class*="adś"], .seznam [class*="adş"]
        if 'oglasi-prodaja' not in item['url']:
            raise DropItem("Broken/weird ad")
        iid = item['iid']
        if iid in self.known_items:
            # If price didnt change -> drop
            if item['price'] == self.known_items[iid]['price']:
                raise DropItem("Known item: %s" % iid)
            # If price changes, remove & treat as new
            else:
                del self.known_items[iid]
                item['desc'] += ' PRICE CHANGED'
        # New
        if iid in self.new_items:
            raise DropItem("Duplicate: %s" % iid)
        self.new_items[iid] = item
        return item

    def close_spider(self, spider):
        # Write everything back to file
        with open(self.db_path, 'w') as f:
            for item in self.known_items.values():
                line = item['date'] + '|' + item['iid'] + '|' + item['price'] + '|' + item['title'] + '|' + item['desc'] + '|' + item['url'] + "\n"
                f.write(line)
            for item in self.new_items.values():
                line = str(date.today()) + '|' + item['iid'] + '|' + item['price'] + '|' + item['title'] + '|' + item['desc'] + '|' + item['url'] + "\n"
                f.write(line)

        # If new ads send email
        if len(self.new_items) > 0:
            mailer = MailSender(
                mailfrom=mail_username,
                smtphost=mail_server,
                smtpport=mail_port,
                smtpuser=mail_username,
                smtppass=mail_password,
                smtpssl=True
            )

            # Mail head
            mail_head = """\
            <html>
            <body>
            """
            # Generate mail body
            mail_body = """"""
            for item in self.new_items.values():
                mail_body += """<p><a href="{0}">{1}</a> {2}<br>{3}</p>""".format(item['url'], item['title'], item['price'], item['desc'])

            mail_search_links = """"""
            for num, link in enumerate(spider.start_urls):
                mail_search_links += """<a href="{}">Link{}</a> """.format(link, str(num + 1))

            mail_foot = """\
            <p>Search manually: {}</p>
            </body>
            </html>
            """.format(mail_search_links)

            # Send
            mail = mailer.send(
                to=spider.mail_to,
                subject="New ads for you - " + spider.name,
                body=mail_head + mail_body + mail_foot,
                mimetype='text/html'
            )
            # Avoid exception: https://github.com/scrapy/scrapy/issues/3478
            return mail
