import scrapy
from scrapy.http import HtmlResponse
from job_parser.items import JobParserItem


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['russia.superjob.ru']

    def __init__(self, vacancy=None):
        super(SuperjobRuSpider, self).__init__()
        self.start_urls = [
            f'https://russia.superjob.ru/vacancy/search/?keywords={vacancy}'
        ]

    def parse(self, response: HtmlResponse, start=True):
        next_page = response.css('a.f-test-link-Dalshe ::attr(href)') \
            .extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.css(
            'div.f-test-vacancy-item \
            a[class*=f-test-link][href^="/vakansii"]::attr(href)'
            ).extract()

        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('div._3MVeX h1 ::text').extract()

        company_name = response.css('h2._15msI ::text').extract()

        company_address = response.css('div.f-test-address span._2JVkc ::text').extract()

        salary = response.css(
            'div._3MVeX span[class="_3mfro _2Wp8I PlM3e _2JVkc"] ::text'
            ).extract()

        vacancy_link = response.url
        site_scraping = self.allowed_domains[0]

        yield JobParserItem(name=name, \
                            company_name=company_name, \
                            company_address=company_address, \
                            vacancy_link=vacancy_link, \
                            salary=salary, \
                            site_scraping=site_scraping
                            )
