# -*- coding: utf-8 -*-
import scrapy

class MyItem(scrapy.Item):

    # ... other item fields ...
    file_urls = scrapy.Field()
    files = scrapy.Field()
    image_names = scrapy.Field()
    pass
    
class SpriteSpider(scrapy.Spider):
    name = 'sprite'
    allowed_domains = ['https://pokemondb.net']
    start_urls = ['https://pokemondb.net/sprites']

    def parse(self, response):
        gen1_list = response.xpath("//h2[@id='gen1']/following-sibling::div[1]")
        links = gen1_list.css("a::attr(href)").getall()

        for link in links:
            absolute_url = self.allowed_domains[0] + link
            yield scrapy.Request(absolute_url, callback=self.parse_img, dont_filter=True)

    def parse_img(item, response):
        img_list = response.css("img::attr(src)").getall()
        item = MyItem()
        item['file_urls'] = img_list
        item['image_names'] = ['-'.join(name.split('/')[4:]) for name in img_list]
        # for i in img_list:
        #     yield {'img' : i}
        return item

