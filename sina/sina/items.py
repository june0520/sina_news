# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    #大类的名称
    category = scrapy.Field()
    # 大类的URL
    category_url = scrapy.Field()
    # 小类的名称
    classify = scrapy.Field()
    # 小类的URL
    classify_url = scrapy.Field()
    #小类目录的存储路径
    sub_filename = scrapy.Field()
    #小类下的子链接
    son_url = scrapy.Field()
    #标题
    title = scrapy.Field()
    #新闻内容
    content = scrapy.Field()
