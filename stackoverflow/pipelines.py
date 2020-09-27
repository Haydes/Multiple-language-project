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
        # text = "id:" + item['_id'] + "\tquestion:" + item['questions'] + "\tvote:" + item['votes'] \
        #     + "\tanswer:" + item['answers'] + "\tview:" + item['views'] +"\tlink: https://stackoverflow.com" + item['links'] \
        #        + "\ttime:" + item['time']
        # if len(item['author']) > 0:
        #     text += "\tauthor:" + item['author'][0] + "\treputation:" + item['reputation'][0]
        text = item['_id'] + "\t" + item['questions'] + "\t" + item['votes'] + "\t" + item['answers'] + "\t" + item['views'] + \
               "\thttps://stackoverflow.com" + item['links'] + "\t" + item['time']
        if len(item['author']) > 0:
            text += "\t" + item['author'][0] + "\t" + item['reputation'][0]
        text += '\n'
        fp.write(text)
        fp.close()
        return item


