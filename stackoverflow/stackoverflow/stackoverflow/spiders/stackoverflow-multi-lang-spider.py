import scrapy

from stackoverflow.items import StackoverflowItem

# https://stackoverflow.com/search?page=2&tab=Votes&q=jython
# https://stackoverflow.com/questions/tagged/java%2bpython?tab=votes&page={}&pagesize=15 (1, 34)
# /questions/tagged/java%2bc?tab=votes&page={}&pagesize=15 (1, 26)
mode = 1 #tagged
# mode = 2 search
class StackoverflowMultiLangSpider(scrapy.Spider):
    name =  "stackoverflow-multi-lang"
    def start_requests(self):
        urls = []
        _url = 'https://stackoverflow.com/questions/tagged/java%2bc?tab=votes&page={}&pagesize=15'

        for page in range(1, 26):
            urls.append(_url.format(page))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        question_list = response.xpath('//*[@id="questions"]')
        if mode == 1:
            for question in question_list.xpath('./div'):
                item = StackoverflowItem()
                item['_id'] = question.xpath('@id').extract()[0].strip('question-summary-')
                item['questions'] = question.xpath('div[2]/h3/a/text()').extract()[0]
                item['votes'] = question.xpath('div[1]/div[1]/div[1]/div/span/strong/text()').extract()[0]
                item['answers'] = question.xpath('div[1]/div[1]/div[2]/strong/text()').extract()[0]
                item['views'] = question.xpath('div[1]/div[2]/@title').extract()[0].strip(' views')
                item['links'] = question.xpath('div[2]/h3/a/@href').extract()[0]
                item['time'] = question.xpath('div[2]/div[3]/div/div[1]/span/text()').extract()[0]
                item['author'] = question.xpath('div[2]/div[3]/div/div[3]/a/text()').extract()
                item['reputation'] = question.xpath('div[2]/div[3]/div/div[3]/div/span[1]/text()').extract()
                yield item
        # elif mode == 2:
        #     for question in question_list.xpath('./div'):
        #         item = StackoverflowItem()
        #         item['_id'] = question.xpath('@id').extract()[0].strip('question-summary-')
        #         item['questions'] = question.xpath('div[2]/h3/a/text()').extract()[0]
        #         item['votes'] = question.xpath('div[1]/div[1]/div[1]/div/span/strong/text()').extract()[0]
        #         item['answers'] = question.xpath('div[1]/div[1]/div[2]/strong/text()').extract()[0]
        #         item['views'] = question.xpath('div[1]/div[2]/@title').extract()[0].strip(' views')
        #         item['links'] = question.xpath('div[2]/h3/a/@href').extract()[0]
        #         item['time'] = question.xpath('div[2]/div[3]/div/div[1]/span/text()').extract()[0]
        #         item['author'] = question.xpath('div[2]/div[3]/div/div[3]/a/text()').extract()
        #         item['reputation'] = question.xpath('div[2]/div[3]/div/div[3]/div/span[1]/text()').extract()
        #         yield item


