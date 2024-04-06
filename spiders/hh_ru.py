import scrapy
from scrapy.http import HtmlResponse
from job_parser.items import JobParserItem
import re


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']

#    start_urls = [
#        'https://hh.ru/search/vacancy?area=2019&st=searchVacancy&text=python'
#        ]

    def __init__(self, vacancy=None):
        super(HhRuSpider, self).__init__()
        self.start_urls = [
            f'https://hh.ru/search/vacancy?area=2019&st=searchVacancy&text={vacancy}'
        ]

    def parse(self, response: HtmlResponse, start=True):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)') \
            .extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.css(
            'div.vacancy-serp \
            div.vacancy-serp-item \
            div.vacancy-serp-item__row_header \
            a.bloko-link::attr(href)'
            ).extract()

        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1.bloko-header-1 ::text').extract()

        company_name = response.css(
            'div.vacancy-company-name-wrapper \
            span.bloko-section-header-2 ::text') \
            .extract()

        company_address = response.css(
            'div.vacancy-company_with-logo \
            p[data-qa="vacancy-view-location"] ::text') \
            .extract()

        salary = response.css('div.vacancy-title p.vacancy-salary ::text').extract()

        vacancy_link = response.url
        site_scraping = self.allowed_domains[0]

        yield JobParserItem(name=name, \
                            company_name=company_name, \
                            company_address=company_address, \
                            vacancy_link=vacancy_link, \
                            salary=salary, \
                            site_scraping=site_scraping
                            )
