
# -*- coding: utf-8 -*-


import gevent.monkey
gevent.monkey.patch_all()

import re
import requests

from sqlalchemy import *
# -*- coding: utf-8 -*-

from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *


engine = create_engine('sqlite:///data.sqlite', echo=True)
Session = sessionmaker(bind=engine)

db = Session()

Base = declarative_base()


class UrlPool(Base):
    __tablename__ = 'url_pool'
    url = Column(String, primary_key=True)
    scanned = Column(Boolean)

class District(Base):
    __tablename__ = 'district'
    code = Column(String, primary_key=True)
    level = Column(Integer)
    name = Column(String)
    in_url = Column(String)
    href = Column(String)
    class_code =Column(String)

url_pool = []

# code, name
items = []

def getText(url):
    r = requests.get(url)
    r.encoding = 'gb2312'
    return r.text


text = getText('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/index.html')
matches = re.finditer(u"<a href='(?P<code>[^.]+).html'>(?P<name>[^<]+)", text)
for m in matches:
    items.append((m.group('code'), m.group('name')))
    url_pool.append('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+
                    m.group('code')+'.html')


def analyse(url):
    text = getText(url)

    matches = re.finditer(
                u"<a href='(?P<url>[^']+)'>(?P<code>[0-9]{12})</a></td>"+
                u"<td><a href='([^.]*).html'>(?P<name>[^<]+)</a>", text)
    for m in matches:
        new_url = url[:url.rindex('/')] + '/' + m.group('url')
        url_pool.append(new_url)
        items.append((m.group('code'), m.group('name')))
    else:
        matches = re.finditer(
            u"<td>(?P<code>[0-9]{12})</td>"+
            u"<td>(?P<class>[0-9]{3})</td>"+
            u"<td>(?P<name>[^<]+)</td>", text)
        for m in matches:
            items.append((m.group('code'), m.group('name')))


while url_pool:
    print len(url_pool)
    url = url_pool[0]
    print url
    url_pool = url_pool[1:]
    analyse(url)

for i in sorted(items):
    print i[0], i[1]
