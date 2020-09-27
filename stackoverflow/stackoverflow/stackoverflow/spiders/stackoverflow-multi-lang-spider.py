import scrapy

from stackoverflow.items import StackoverflowItem

mode = 1 #tagged
# mode = 2 search
class StackoverflowMultiLangSpider(scrapy.Spider):
    name =  "stackoverflow-multi-lang"
    def start_requests(self):
        urls = []
        _url = 'https://stackoverflow.com'
        href = "/questions/tagged/python%20c%2b%2b%20c%23"
        sortByVotes = "?tab=Votes"

        _url += href + sortByVotes

        for page in range(1, 10):
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
                item['time'] = question.xpath('div[2]/div[3]/div/div[1]/span/@title').extract()[0].strip('Z')
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


