import scrapy
import json
from urllib.parse import urlencode
from datetime import datetime

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com', 'i.instagram.com']
    start_urls = ['https://www.instagram.com/']

    _login_url = '/accounts/login/ajax/'
    _tag_path = '/explore/tags/'
    _api_url = 'https://i.instagram.com/api/v1/tags/'
    _graphql_q_url = 'https://www.instagram.com/graphql/query/'
    _q_hash = 'd4e8ae69cb68f66329dcebe82fb69f6d'
    _app_id = '936619743392459'
    _instagram_ajax = '822bad258fea'

    def __init__(self, login, password, tags, *args, **kwargs):
        self.login = login
        self.password = password
        self.tags = tags
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        try:
            json_data = self._js_data_extract(response)
            csrf_token = json_data["config"]["csrf_token"]
            yield scrapy.FormRequest(
                response.urljoin(self._login_url),
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.password,
                    'queryParams': '{"hl":"ru"}',
                    'optIntoOneTap': 'false'
                },
                headers={
                    'x-csrftoken': csrf_token,
                    'x-instagram-ajax': self._instagram_ajax,
                    'x-ig-app-id': self._app_id,
                    'x-requested-with': 'XMLHttpRequest'
                }
            )
        except AttributeError:
            if response.json().get('authenticated'):
                for tag in self.tags:
                    yield response.follow(
                        f'{self._tag_path}{tag}/',
                        callback=self.tag_page_parse,
                        cb_kwargs={'tag': tag, 'page': 0}
                    )

    def tag_page_parse(self, response, **kwargs):
        if 'explore' in response.url:
            json_data = self._js_data_extract(response)
            csrf_token = json_data["config"]["csrf_token"]
            recent_data = json_data['entry_data']['TagPage'][0]['data']['recent']
        else:
            csrf_token = kwargs['csrf_token']
            recent_data = response.json()
        tag = kwargs['tag']
        next_max_id = recent_data['next_max_id']
        page = recent_data['next_page']
        if recent_data['more_available']:
            yield scrapy.FormRequest(
                response.urljoin(f'{self._api_url}{tag}/sections/'),
                method='POST',
                callback=self.tag_page_parse,
                formdata={
                    'max_id': str(next_max_id),
                    'page': str(page),
                    'tab': 'recent',
                },
                headers={
                    'x-csrftoken': csrf_token,
                    'x-ig-app-id': self._app_id,
                },
                cb_kwargs={'tag': tag, 'page': page, 'csrf_token': csrf_token}
            )
        for raw in recent_data['sections']:
            for entry in raw['layout_content']['medias']:
                yield response.follow(
                    self.post_url_forming(entry['media']['code']),
                    callback=self.post_parse,
                    cb_kwargs={'tag': tag, 'page': 0}
                )

    def post_url_forming(self, media_code):
        variables = {'shortcode': media_code}
        params = {'query_hash': self._q_hash, 'variables': json.dumps(variables)}
        parametric_url = f'{self._graphql_q_url}?{urlencode(params)}'
        return parametric_url

    def post_parse(self, response, **kwargs):
        print(1)
        data = response.json()['data']['shortcode_media']
        item = {
            'date_parse': datetime.now(),
            'tag': kwargs['tag'],
            'data': data
        }
        yield item


    def _js_data_extract(self, response):
        script = response.xpath('//script[contains(text(), "window._sharedData = ")]/text()').extract_first()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])
