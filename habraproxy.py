#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

from bs4 import BeautifulSoup

# ...
from flask import Flask
from werkzeug.routing import BaseConverter


app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/company/<regex("[a-z]+"):company_name>/blog/<regex("\d+"):blog_id>/')
def go(company_name,blog_id):
    # ...
    url = 'https://habrahabr.ru/company/%(company_name)s/blog/%(blog_id)s/'%dict(
        company_name=company_name,
        blog_id=blog_id
    )
    # ...
    def replacer(match):
        return match.group().upper()+'(TM)'
    # ...
    # p = re.compile(ur'(?!<[^>]*?)((?<=[^a-zA-Zа-яА-Я])[a-zA-Zа-яА-Я]{6}(?=[^a-zA-Zа-яА-Я]))(?![^<]*?>)',re.MULTILINE)    
    p = re.compile(ur'((?<=^)|(?<=[\s\n]))[a-zA-Zа-яА-Я]{6}((?=[\s\n,\.])|(?=$))',re.MULTILINE)    
    """
    """
    # ...
    content = requests.get(url).content
    page = BeautifulSoup(content,"lxml")
    div = page.find("div", {"class": "content html_format"})
    # ...
    allTags = div.findAll(text=p)
    for tag in allTags:
        tag.replaceWith(p.sub(replacer, tag))

    return str(page)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
    # http://127.0.0.1:8000/company/yandex/blog/258673/