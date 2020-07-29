# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):
    game_name = scrapy.Field()
    box_txt = scrapy.Field()
    game_tag = scrapy.Field()
    detail_url = scrapy.Field()
    game_intro = scrapy.Field()
    game_fever = scrapy.Field()
    game_fav = scrapy.Field()
    game_neg = scrapy.Field()
    feedback_rate = scrapy.Field()
    game_avg = scrapy.Field()

