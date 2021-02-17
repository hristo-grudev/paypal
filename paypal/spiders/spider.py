import scrapy

from scrapy.loader import ItemLoader
from ..items import PaypalItem
from itemloaders.processors import TakeFirst


class PaypalSpider(scrapy.Spider):
	name = 'paypal'
	start_urls = ['https://newsroom.paypal-corp.com/news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="wd_title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@aria-label="Show next page"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="wd_title wd_language_left"]/text()').get()
		description = response.xpath('//div[@class="wd_subtitle wd_language_left"]//text()|//div[@class="wd_body wd_news_body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="wd_date"]/text()').get()

		item = ItemLoader(item=PaypalItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
