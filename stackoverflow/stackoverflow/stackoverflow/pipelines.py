# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class StackoverflowPipeline(object):

    # + " author:" + item['author']
    # + " reputation:" + item['reputation']
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = base_dir +'/data.txt'
        fp = open(filename, 'a')
        text = "id:" + item['_id'] + " question:" + item['questions'] + " vote:" + item['votes'] \
            + " answer:" + item['answers'] + " view:" + item['views'] +" link: https://stackoverflow.com" + item['links'] \
               + " time:" + item['time']
        if len(item['author']) > 0:
            text += " author:" + item['author'][0] + " reputation:" + item['reputation'][0]
        text += '\n'
        fp.write(text)
        fp.close()
        return item


