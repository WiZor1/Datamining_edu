import os
import dotenv

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson7.instagram_parse.spiders.instagram import InstagramSpider


if __name__ == "__main__":
    dotenv.load_dotenv(".env", override=True)
    crawler_settings = Settings()
    crawler_settings.setmodule("instagram_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    tags = ['python', 'programming']
    crawler_proc.crawl(
        InstagramSpider,
        login=os.getenv("USERNAME"),
        password=os.getenv("ENC_PASSWORD"),
        tags=tags,
    )
    crawler_proc.start()
