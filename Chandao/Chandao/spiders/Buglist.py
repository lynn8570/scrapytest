# -*- coding: utf-8 -*-
import scrapy

from Chandao.items import ChandaoItem

class BuglistSpider(scrapy.Spider):
    name = 'Buglist'
    #allowed_domains = ['http://192.168.2.27/']
    #start_urls = ['http://192.168.2.27/user-login-Lw==.html']
    start_urls =  ['http://192.168.2.27/zentao/bug-browse-21.html']
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'account':'linlian','password':'123456'},
            callback = self.after_login
        )

    def after_login(self,response):
        print("after......")
        print(response.body)
        print(response.url)
        print(response.xpath('//script').extract()[0])
        #with open("body.txt", 'wb') as f:
        #    f.write(response.body)
        #b"<script>parent.location='/zentao/index.html';\n\n</script>\n"
        return scrapy.Request('http://192.168.2.27/zentao/bug-browse-21.html',
                              callback= self.parse_buglist)
    def parse_buglist(self,response):
        print("parse_buglist")


        node_list = response.xpath("//tr[@class='text-center']")
        for node in node_list:
            item =  ChandaoItem()
            item['severity'] = node.xpath("./td[2]/span/text()").extract()[0]
            item['title'] = node.xpath("./td[4]/a/text()").extract()[0]
            item['founder'] = node.xpath("./td[5]/text()").extract()[0]
            item['current'] = node.xpath("./td[6]/text()").extract()[0]
            yield item

        try:
            url = response.xpath("//i[@class='icon-play']/../@href").extract()[0]
            print(url)
            if len(url) !=0:
                yield scrapy.Request('http://192.168.2.27'+url,callback=self.parse_buglist)
        except IndexError:
            print("Get next Error")

    #scrapey crawl Buglist -o items.json
