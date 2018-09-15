import scrapy
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
        ville, arrondissement, code_postal = response.css('div.item-description h2::text').re(r'\w+')
        corps = ' '.join(map(self.clean_text, response.css('div.item-description p::text').extract()))
        tags = list(map(clean_text, response.css('ul.item-tags li strong::text').extract()))
        loyer = ''.join(response.css('span.item-price::text').re(r'\d+'))
        metros = self.get_metro()
        titre, prix = map(lambda x: normalize('NFKD', x), response.css('h1.item-title span::text').extract())
        photo_is_present = bool(response.css('div.owl-carousel').extract())
        contact_tel = ''.join(response.css('div.sidebar strong.tel-wrapper').re(r'\d{2}'))
        ref = response.css('p.item-date::text').extract_first()
        url = response.url
        temps_de_trajet = min(map(get_travel_time_from, metros))

    def clean_text(self, html_scrapped):
        trans_table = {ord(c): None for c in u'\r\n\t'}
        return normalize('NFKD', html_scrapped.translate(trans_table))

    def get_metro(self):
        pass
        # Checker si il y a metro dans le nom
        # append
        # return
        # item_transports = response.css('ul.item-transports')
        # stations_a_proximite = []
        # lignes = []
        # for item in item_transports:
        #     station = item.css('span.label::text').extract_first()
        #     if station:
        #         stations_a_proximite.append(station)
        #     ligne = item.css('span.icon::attr("class")').extract()
        #     if ligne:
        #         ligne = ligne[1].replace('icon ', '')
        #         lignes.append(ligne)
        # return stations_a_proximite, lignes

    