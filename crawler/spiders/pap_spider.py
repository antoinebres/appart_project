# -*- coding: utf-8 -*-
import scrapy
from appart_project.items import Annonce
from unicodedata import normalize
from citymapper_service import get_travel_time_from

class papSpider(scrapy.Spider):
    name = "pap.fr"
    start_urls = [
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-2',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-3',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-4',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-5',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-6',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-7',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-8',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-9',
        'https://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-1100-euros-a-partir-de-25-m2-10',
    ]

    def parse(self, response):
        # Get links
        liste_url_annonces = list(set(response.css('a::attr("href")').re(r'annonces\/.*')))
        for url_annonce in liste_url_annonces:
            if url_annonce is not None:
                yield response.follow(url_annonce, self.parse_annonce)


    def parse_annonce(self, response):
        annonce = Annonce()
        annonce['ville'], annonce['arrondissement'], annonce['code_postal'] = response.css('div.item-description h2::text').re(r'\w+')
        annonce['corps'] = ' '.join(map(self.clean_text, response.css('div.item-description p::text').extract()))
        annonce['tags'] = list(map(self.clean_text, response.css('ul.item-tags li strong::text').extract()))
        annonce['loyer'] = ''.join(response.css('span.item-price::text').re(r'\d+'))
        annonce['lignes'], annonce['stations'] = self.get_metro(response)
        annonce['titre'], _ = map(lambda x: normalize('NFKD', x), response.css('h1.item-title span::text').extract())
        annonce['photo_is_present'] = bool(response.css('div.owl-carousel').extract())
        annonce['contact_tel'] = ''.join(response.css('div.sidebar strong.tel-wrapper').re(r'\d{2}'))
        annonce['ref'] = response.css('p.item-date::text').extract_first()
        annonce['url'] = response.url
        annonce['temps_de_trajet'] = min(map(get_travel_time_from, annonce['stations']))
        return annonce

    def clean_text(self, html_scrapped):
        trans_table = {ord(c): None for c in u'\r\n\t'}
        return normalize('NFKD', html_scrapped.translate(trans_table))

    def get_metro(self, response):
        lignes = list(set(filter(lambda x: x != '0', response.css('ul.item-transports span::attr(class)').re(r'metro-(\d+.*)'))))
        stations = response.css('ul.item-transports span::text').extract()
        return lignes, stations

        # TODO
        # Enlever les stations qui ne sont pas dans Paris dans stop_coords
        # Define:
        # - Chapelle
    