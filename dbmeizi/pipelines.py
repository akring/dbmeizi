# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import json
import urllib
import os

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Meizi added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item


# 根目录下生成JSON文件
class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

        return item


# 检查并去重
class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['datasrc'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['datasrc'])
        return item


# 图片写入本地
class WriteToDiskPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):

        link = item['datasrc']
        title = item['title']

        filefolder = '/Users/akring/Desktop/pic'
        filesavepath = '/Users/akring/Desktop/pic/%s.png' % title

        # 如果路径不存在，则创建路径
        if not os.path.exists(filefolder):
            os.mkdir(filefolder)

        # 如果存在重名文件，则不再次下载
        if os.path.exists(filesavepath) and os.path.isfile(filesavepath):
            print ("File already exists")
        else:
            print link
            urllib.urlretrieve(link, filesavepath)

        return item
