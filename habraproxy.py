#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import sys
# ..
from bs4 import BeautifulSoup
# ...
from flask import Flask, request
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter


@app.route('/', methods=['GET', 'POST'])
def start():
    content = '''
    Habraproxy is works! </br>
    **************************************************************** </br>
    please follow this link <a
        href = "http://{0}/company/yandex/blog/258673/">
        http://{0}/company/yandex/blog/258673/</a>
    '''.format(request.headers['Host'])
    return content


@app.route(
    '/company/<regex("[a-z]+"):compnam>/blog/<regex("\d+"):blogid>/')
def proxy(compnam, blogid):
    # ...
    url = 'https://habrahabr.ru/company/%(compnam)s/blog/%(blogid)s/' % dict(
        compnam=compnam,
        blogid=blogid
    )

    def replacer(match):
        return match.group().upper()+'(TM)'
    # ...
    p = re.compile(
        ur'((?<=^)|(?<=[\s\n]))[a-zA-Zа-яА-Я]{6}((?=[\s\n,\.])|(?=$))',
        re.MULTILINE
    )
    # ...
    content = requests.get(url).content
    page = BeautifulSoup(content, 'html.parser')
    div = page.find("div", {"class": "content html_format"})
    # ...
    allTags = div.findAll(text=p)
    for tag in allTags:
        tag.replaceWith(p.sub(replacer, tag))

    return str(page)

if __name__ == '__main__':
    hp = sys.argv[1].split(':')
    host = hp[0]
    port = int(hp[1])
    # ...
    app.run(host=host, port=port, debug=True)
