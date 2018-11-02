# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#
# class SinaPipeline(object):
#     def process_item(self, item, spider):
#         title = item['title']
#         filename = title[1:-1] + '.txt'
#         with open(item['sub_filename']+'/'+ filename, 'w') as f:
#             f.write(item['content'])
#             return item


class SinaPipeline(object):
    def process_item(self, item, spider):
        son_url = item['son_url']
        filename = son_url[7:-6].replace('/', '-')
        filename += '.txt'
        f = open(item['sub_filename']+'/'+filename, 'wb')
        f.write(item['content'].encode('utf8'))
        f.close()
        return item

