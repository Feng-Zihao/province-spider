
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

#import gevent.monkey
#gevent.monkey.patch_all()

import re
import requests

from sqlalchemy import *

from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *


engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)

db = Session()

Base = declarative_base()


class UrlPool(Base):
    __tablename__ = 'url_pool'
    url = Column(String, primary_key=True)
    level = Column(Integer)
    scanned = Column(Boolean)

class District(Base):
    __tablename__ = 'district'
    code = Column(String, primary_key=True)
    level = Column(Integer)
    name = Column(String)
    page_url = Column(String)
    href = Column(String)
    class_code =Column(String)

url_pool = []


def getText(url):
    r = requests.get(url)
    r.encoding = 'gb2312'
    return r.text


def scanHomePage():
    text = getText('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/index.html')
    matches = re.finditer(u"<a href='(?P<code>[^.]+).html'>(?P<name>[^<]+)", text)
    for m in matches:
        district = District(
            code=m.group('code'),
            level=1,
            name=m.group('name'),
            page_url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/index.html',
            href='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+
                 m.group('code')+'.html'
        )
        url_pool = UrlPool(
            url=district.href,
            level=1,
            scanned=False)
        db.add(district)
        db.add(url_pool)
    db.commit()


def analyse(url, current_level):
    text = getText(url)

    matches = re.finditer(
                u"<a href='(?P<url>[^']+)'>(?P<code>[0-9]{12})</a></td>"+
                u"<td><a href='([^.]*).html'>(?P<name>[^<]+)</a>", text)
    for m in matches:
        new_url = url[:url.rindex('/')] + '/' + m.group('url')
        district = District(
            code=m.group('code'),
            level=current_level + 1,
            name=m.group('name'),
            page_url=url,
            href=new_url
        )
        url_pool = UrlPool(
            url=district.href,
            level=current_level + 1,
            scanned=False)
        db.add(district)
        db.add(url_pool)
    else:
        matches = re.finditer(
            u"<td>(?P<code>[0-9]{12})</td>"+
            u"<td>(?P<class_code>[0-9]{3})</td>"+
            u"<td>(?P<name>[^<]+)</td>", text)
        for m in matches:
            district = District(
                code=m.group('code'),
                level=current_level + 1,
                name=m.group('name'),
                page_url=url,
                class_code=m.group('class_code')
            )
            db.add(district)
    db.commit()


#scanHomePage()
while true:
    url_pool = db.query(UrlPool).filter_by(scanned=False).first()
    if url_pool is None:
        break
    print url_pool.level, url_pool.url
    analyse(url_pool.url, url_pool.level)
    url_pool.scanned = True
    db.add(url_pool)
    db.commit()

