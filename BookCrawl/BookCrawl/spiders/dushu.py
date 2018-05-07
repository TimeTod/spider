# -*- coding: utf-8 -*-
import scrapy
from BookCrawl.items import BookcrawlItem


class DushuSpider(scrapy.Spider):
    name = 'dushu'
    allowed_domains = ['dushu.com']
    start_urls = ['https://www.dushu.com/news/99.html']

    def parse(self, response):
        item = BookcrawlItem()
        book_contents = response.css('body > div.container.margin-top > div.news-left > div.news-list > div')
        for book in book_contents:

            name = book.css('h3 > a').xpath('string(.)').extract_first()
            desc = book.xpath('p[@class="news-item-text"]/text()').extract_first()
            url = 'https://www.dushu.com'
            links = book.css('::attr("href")').extract_first()
            final_urls = url + links

            item['name'] = name
            item['desc'] = desc
            request = scrapy.Request(final_urls,callback=self.parse_detail)
            request.meta['item'] = item
            yield request
            # yield scrapy.Request(final_urls,callback=self.parse)
            # print(name)
            # with open('dushu.html','wb') as f:
            #     f.write(response.body)
            # soup = BeautifulSoup(response.body,'lxml')
            # divs = soup.find_all(name='div',class_='news-item')
            next_page = response.xpath('.//div[@class="page"]/a/@href')[-1]
            if next_page is not None:
                page_url = url + next_page.extract()
                request = scrapy.Request(page_url,callback=self.parse)
                yield request

            # for div in divs:
            #     title = div.select('h3')
            #     title_link = title.a.get('href')
            #     print(title_link)
            #     print(title_link.get_text())
            #     request = scrapy.Request(title_link,callback=self.parst_detail)
            #     yield request

        # def get_detail(self,response):
        #     # content_detail = response.xpath('//div[@class="news-left"]/text()').extract_first()
        #     # print(content_detail)
        #     pass


    def parse_detail(self,response):
        item = response.meta['item']
        detail = response.xpath('//div[@class="news-left"]/div/div[@class="text"]/p/text()').extract_first()
        item['detail'] = detail
        yield item
