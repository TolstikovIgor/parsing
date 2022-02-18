# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instagramparser.items import InstagramparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from pprint import pprint


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = "dedparser"
    insta_pwd = "#PWD_INSTAGRAM_BROWSER:10:1616865878:AZlQADP6pk/5VnFe5bKuY6T9kfTDmBUXYn9qdQB7m7meM6h2CgQb4HSz0pHmNBOnRMjPK0Ahzgub9y7qT+cttle277sc8E7/1xPlM1SnjAw+nGDpITS23K3IzDB1G1Sqz+IOdnnaLmTfNAZu/nojpEw="
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['ostrov_salon', 'texaspizzeria', 'makcim123098']

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash1 = '18a7b935ab438c4514b1f742d8fa07a7'
    subscription_hash = 'd04b0a864b4b54837c0d870b0e77e076'
    subscriber_hash = 'c76146de99bb02f6415203be841dd25a'

    subscriptions = {}

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.myuser_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={"X-CSRFToken": self.fetch_csrf_token(response.text)}
        )

    def myuser_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        for parse_user in self.parse_users:
            if j_body['authenticated']:
                yield response.follow(
                    f'/{parse_user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'person_name': parse_user}
                )

    def user_data_parse(self, response: HtmlResponse, person_name):
        person_id = self.fetch_person_id(response.text, person_name)
        variables = {"id": person_id,
                     "first": 25}

        url_posts = f'{self.graphql_url}query_hash={self.subscriber_hash}&variables=' + json.dumps(variables,
                                                                                                   separators=(
                                                                                                   ',', ':'))

        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'person_name': person_name,
                       'person_id': person_id,
                       'followto_id': person_id,
                       'variables': deepcopy(variables)}
        )

        url_posts = f'{self.graphql_url}query_hash={self.subscription_hash}&variables=' + json.dumps(variables,
                                                                                                     separators=(
                                                                                                     ',', ':'))
        followto_id = None
        if person_id not in self.subscriptions:
            self.subscriptions[person_id] = []
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'person_name': person_name,
                       'person_id': person_id,
                       'followto_id': None,
                       'variables': deepcopy(variables)}
        )

    def user_posts_parse(self, response: HtmlResponse, person_name, person_id, followto_id,
                         variables):
        j_data = json.loads(response.text)

        if (followto_id):
            user_info = j_data.get('data').get('user').get('edge_followed_by')
            posts_hash = self.subscriber_hash
        else:
            user_info = j_data.get('data').get('user').get('edge_follow')
            posts_hash = self.subscription_hash

        users = user_info.get('edges')
        for user in users:
            item = InstagramparserItem(
                user_id=user['node']['id'],
                photo=user['node']['profile_pic_url'],
                node=user['node'],
                fullname=user['node']['full_name'],
                username=user['node']['username'],
                subscriptions=[followto_id]
            )
            if not followto_id:
                self.subscriptions[person_id].append(user['node']['id'])

            yield item

        if user_info.get('page_info').get('has_next_page'):
            variables['after'] = user_info['page_info']['end_cursor']
            url_posts = f'{self.graphql_url}query_hash={posts_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'person_name': person_name,
                           'person_id': person_id,
                           'variables': deepcopy(variables),
                           'followto_id': followto_id}
            )
        else:
            person_item = InstagramparserItem(
                user_id=person_id,
                photo=response.xpath('//div[@class="XjzKX"]//img/@src'),
                fullname=response.xpath('//h1/text()'),
                username=person_name,
                subscriptions=self.subscriptions[person_id]
            )
            yield person_item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_person_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def fetch_user_fullname(self, text, username):
        matched = re.search(
            '{\"full_name\":\"\\.+\",\"has_ar_effects\":}', text
        ).group()
        return json.loads(matched).get('id')
