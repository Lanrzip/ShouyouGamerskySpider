# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from game.items import GameItem


class GameSpiderSpider(CrawlSpider):
    name = 'game_spider'
    allowed_domains = ['shouyou.gamersky.com']
    start_urls = ['https://shouyou.gamersky.com/ku/0-0-0-30_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+ku\/0-0-0-\d+_\d+\.html'),follow=True),
        Rule(LinkExtractor(allow=r'.+\/ku\/\d+\.shtml'),callback="parse_detail",follow=True),
    )

    def parse_detail(self, response):
        game_name = response.xpath("//span[@class='tit']/text()").get()
        box_txt = response.xpath("//div[@class='box_txt']/text()").get()
        game_tag = ';'.join(response.xpath("//div[@class='box_tag']//text()").getall()).strip()
        game_fav = response.xpath("//span[@id='like']/text()").get()
        game_fever = ''.join(response.xpath("//div[@class='RD']//text()").getall())
        game_neg = response.xpath("//span[@id='unlike']/text()").get()
        feedback_rate = response.xpath("//div[@id='Sorce']/text()").get()
        game_avg = response.xpath("//div[@id='scoreAvg']/text()").get()
        detail_url = response.url
        game_intro = ";".join(response.xpath("//div[@class='Intro']/p/text()").getall()).replace('\u3000','')
        # print(game_avg),'%%%%%%%%%%%%%%%%%%%%%%'
        # print(game_neg,'$$$$$$$$$$$$$$$$$$$$$')
        # print(game_fever,'###################')
        # print(game_fav,'@@@@@@@@@@@@@@@@@@')
        # print(feedback_rate,'!!!!!!!!!!!!!!!!!')

        item = GameItem(
            game_name=game_name,
            box_txt=box_txt,
            game_tag=game_tag,
            detail_url=detail_url,
            game_intro=game_intro,
            game_fav=game_fav,
            game_fever=game_fever,
            game_neg=game_neg,
            feedback_rate=feedback_rate,
            game_avg=game_avg
        )

        yield item