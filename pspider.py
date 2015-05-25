
# -*- coding: utf-8 -*-


import gevent.monkey
gevent.monkey.patch_all()

import re
import requests

r= requests.get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/index.html')
r.encoding = 'gb2312'




provinces  = re.finditer(u"<a href='(?P<code>[^.]+).html'>(?P<province>[^<]+)", r.text)
for p in provinces:
    print p.group('code'), p.group('province')
