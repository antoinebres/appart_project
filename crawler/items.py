# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Annonce(scrapy.Item):
    ref = scrapy.Field()
    url = scrapy.Field()
    titre = scrapy.Field()
    loyer = scrapy.Field()
    tags = scrapy.Field()
    photo_is_present = scrapy.Field()
    ville = scrapy.Field()
    code_postal  = scrapy.Field()
    arrondissement = scrapy.Field()
    corps = scrapy.Field()
    lignes = scrapy.Field()
    stations = scrapy.Field()
    temps_de_trajet = scrapy.Field()
    contact_tel = scrapy.Field()