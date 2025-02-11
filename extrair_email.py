import re

import scrapy


class EmailSpider(scrapy.Spider):
    name = "email_spider"
    #Inserir o site aqui!
    start_urls = ["#"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emails_set = set()
        self.email_count = 0
        self.max_emails = 250

    def parse(self, response):

        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text)

        for email in emails:
            if email not in self.emails_set and self.email_count < self.max_emails:
                self.emails_set.add(email)
                self.email_count += 1
                yield {"email": email}

            if self.email_count >= self.max_emails:
                self.crawler.engine.close_spider(self, reason="Limite de emails atingido!")
                return

        for href in response.css("a::attr(href)").getall():
            if self.email_count < self.max_emails:
                yield response.follow(href, self.parse)
