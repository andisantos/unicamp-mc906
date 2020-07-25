# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class PokescrapPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename','')

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            splits = image_url.split('/')
            meta = {'filename': splits[-1][:-4] +'-'+ '-'.join(splits[4:-1])+'.jpg'}
            yield scrapy.Request(url=image_url, meta=meta)
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item