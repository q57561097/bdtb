#coding:utf-8
from scrapy.spider import Spider
from scrapy.http import Request
from bdtb.items import BdtbItem
import re
import os
class Bdtb(Spider):
    name = "bdpc"
    item=BdtbItem()
    start_urls=["http://tieba.baidu.com/f?kw=%E5%B0%8F%E8%AF%B4%E5%90%A7&ie=utf-8&t=12&fr=news"]
    bg={}
    def parse(self, response):
        host='http://tieba.baidu.com'
        url3='?see_lz=1&pn=1'
        rel = re.compile(r'<a href="(.*?)" title="【原创小说】(.*?)"[\s\S]*?title="主题作者:(.*?)"')
        rest=re.findall(rel,response.body)
        for d in rest:
            auth=d[2]
            title=d[1]
            url=d[0]
            url2=host+url+url3
            if not os.path.exists('/home/zyh/bdtb/%s'%auth):
                os.mkdir('/home/zyh/bdtb/%s'%auth)
            yield Request(url2,meta={'auth':auth,'title':title},callback=self.next_page)
        nextpg=response.xpath('//a[@class="next pagination-item "]/@href').extract()
        if nextpg:
            yield Request(nextpg[0],callback=self.parse)
        yield self.item
    def next_page(self, response):

        title=response.meta['title']
        auth=response.meta['auth']
        title1=title.replace(' ','')
        if '/' in title1:
           title1=title1.replace('/','')


        cont=response.xpath('//div[@class="d_post_content j_d_post_content "]//text()').extract()
        with open('/home/zyh/bdtb/%s/%s.txt'%(auth,title1),'a') as f:
            for i in cont :
              f.write(i+'\n\n')
        rel=re.compile(r'<a href="(.*?)">下一页</a>')
        page=re.findall(rel,response.body)
        host='http://tieba.baidu.com'
        if page:
            nextpage=host+page[0]
            print nextpage
            yield Request(nextpage,callback=self.parse)
        yield self.item


