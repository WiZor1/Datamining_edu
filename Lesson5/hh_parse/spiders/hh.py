import scrapy
from Lesson5.hh_parse.loaders import HhVacancyLoader, HhEmployerLoader


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['krasnodar.hh.ru']
    start_urls = ['https://krasnodar.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    _xpath_selectors = {
        'pagination': '//div[@data-qa="pager-block"]//@href',
        'vacancy': '//div[@class="vacancy-serp-item__info"]//'
                   'a[@data-qa="vacancy-serp__vacancy-title"]/@href',
        'employer': '//div[@class="vacancy-serp-item__info"]//'
                    'div[@class="vacancy-serp-item__meta-info-company"]/a/@href',
    }

    _xpath_vacancy_data_q = {
        'name': '//h1[@data-qa="vacancy-title"]/text()',
        'salary': '//p[@class="vacancy-salary"]//text()',
        'description': '//div[@class="vacancy-description"]//div[@data-qa="vacancy-description"]//text()',
        'skills': '//div[@class="vacancy-section"]//div[@class="bloko-tag-list"]//text()',
    }

    _xpath_vacancy_data_q_custom = {
        'name': '//div[@class="tmpl_hh_wrapper"]//p[@class="tmpl_hh_title"]//text()',
        'salary': '//p[@class="vacancy-salary"]//text()',
        'description': '//div[@class="tmpl_hh_wrapper"]//div[@itemprop="description"]//text()',
        'skills': '//div[@class="vacancy-section"]//div[@class="bloko-tag-list"]//text()',
    }

    _xpath_employer_data_q = {
        'name': '//div[@class="company-header"]//span[@class="company-header-title-name"]/text()',
        'fields_of_activity': '//div[@class="employer-sidebar-content"]/div[@class="employer-sidebar-block"]/p/text()',
        'description': '//div[@class="company-description"]//text()',
        'url': '//div[@class="employer-sidebar-content"]//a[@data-qa="sidebar-company-site"]/@href'
    }

    _xpath_employer_data_q_custom = {
        'name': '//div[@class="company-header"]//span[@class="company-header-title-name"]/text()',
        'fields_of_activity': '//script[@data-name="HH/VacancyGrouping/LoadVacancies"]/@data-params',
        'description': '//div[@class="company-description"]//text()',
        'url': '//div[@class="wrap_hh-wrapper"]//div[@class="wrap_hh_header"]//a/@href'
    }

    def parse(self, response, **kwargs):
        yield from self._get_follow_xpath(
            response, self._xpath_selectors['pagination'], self.parse
        )
        yield from self._get_follow_xpath(
            response, self._xpath_selectors['vacancy'], self.parse_vacancy
        )
        yield from self._get_follow_xpath(
            response, self._xpath_selectors['employer'], self.parse_employer
        )

    def parse_vacancy(self, response):
        loader = HhVacancyLoader(response=response)
        loader.add_value('url', response.url)
        for key, selector in self._xpath_vacancy_data_q.items():
            if not loader.get_xpath(selector):
                loader.add_xpath(key, self._xpath_vacancy_data_q_custom[key])
            else:
                loader.add_xpath(key, selector)
        yield loader.load_item()

    def parse_employer(self, response):
        loader = HhEmployerLoader(response=response)
        loader.add_value('hh_url', response.url)
        if response.xpath(self._xpath_employer_data_q['name']):
            loader.add_value('employer_ad_type', 'standard')
            for key, selector in self._xpath_employer_data_q.items():
                loader.add_xpath(key, selector)
        else:
            loader.add_value('employer_ad_type', 'custom')
            for key, selector in self._xpath_employer_data_q_custom.items():
                loader.add_xpath(key, selector)
        yield loader.load_item()

    @staticmethod
    def _get_follow_xpath(response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)
