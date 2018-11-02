# -*- coding: utf-8 -*-
'''利用scrapy.Spider 类爬取新闻类，因为每个大类下的页面结构不一致所以只爬取到部分页面
后续还是尝试使用crawl类比较好'''
import scrapy
import os
from sina.items import SinaItem


class SinanewsSpider(scrapy.Spider):
    name = 'sinanews'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        items = []
        categories = response.xpath("//div[@class='section']//h3/a/text()").extract()
        category_urls = response.xpath("//div[@class='section']//h3/a/@href").extract()
        classifies = response.xpath("//ul[@class='list01']/li/a/text()").extract()
        classify_urls = response.xpath("//ul[@class='list01']/li/a/@href").extract()
        #遍历大类若不存在并创建目录

        for i in range(0, len(categories)):
            categories_filename = './Data/' + categories[i]
            if not os.path.exists(categories_filename):
                os.mkdir(categories_filename)
                # 遍历小类若不存在创建目录

                for j in range(0, len(classifies)):
                    item = SinaItem()
                    item['category'] = categories[i]
                    item['category_url'] = category_urls[i]

                    if_belong = classify_urls[j].startswith(item['category_url'])
                    if if_belong:
                        sub_filename = categories_filename + '/' + classifies[j]
                        if not os.path.exists(sub_filename):
                            os.mkdir(sub_filename)
                        item['classify'] = classifies[j]
                        item['classify_url'] = classify_urls[j]
                        item['sub_filename'] = sub_filename
                        items.append(item)

         #遍历小类的URL发送请求，得到response连同包含的meta数据一起提交给回调函数
        for item in items:
            yield scrapy.Request(item['classify_url'], meta={'meta_1': item}, callback=self.item_parse)

                    #处理小类的页面
    def item_parse(self, response):
        #提取每次response的meta数据
        meta_1 = response.meta['meta_1']
        #标题新闻链接
        son_urls = response.xpath("//ul[@class='news-2']//a/@href").extract()
        items = []
        for i in range(0, len(son_urls)):
            # if_belong = son_urls[i].startswith(meta_1['classify_url']) and son_urls[i].endswith('.shtml')
            # if if_belong:
            #获取字段的值，并保存到item中，便于传输
            item = SinaItem()
            item['category'] = meta_1['category']
            item['category_url'] = meta_1['category_url']
            item['classify'] = meta_1['classify']
            item['classify_url'] = meta_1['classify_url']
            item['sub_filename'] = meta_1['sub_filename']
            item['son_url'] = son_urls[i]
            items.append(item)

        for item in items:
            yield scrapy.Request(item['son_url'], meta={'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']
        # 新闻标题
        title = response.xpath("//h1[@class='main-title']/text()").extract()
        #新闻的内容正文
        contents = response.xpath("//div[@class='article']/p/text()").extract()
        content = ''.join(contents)
        # 标题
        item['title'] = title
        # 新闻内容
        item['content'] = content

        yield item



