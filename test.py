from lxml import html
from lxml import etree
import re
import time

# import centipede.stackexchange.unix.questions as site
# import centipede.stackexchange.unix.qna as site
import centipede.linuxquestions.list as site
# import centipede.linuxquestions.thread as site


debug_mode = True
log = True
log_print = True
    

# cookies = dict(unixuser="t=&s=&p=[2|2][10|50]")
# params = {'sort': 'newest', 'pagesize': '50', 'page': '1'}
# r = requests.get('http://unix.stackexchange.com/questions/tagged/security', params=params, headers=headers)


with open('linuxquestions.html', 'rb') as fp:
# with open('stackexchange.unix.qna.html', 'rb') as fp:
    tree = html.fromstring(fp.read())

elements = tree.xpath(site.elements['path'])

# print len(elements)
# Quicknote: xpath always return a "list" of elements no matter how many items
#            are matched

# print site.elements['path']
# print elements

dlist = list()
ts = time.time()

for e in elements:
    d = {}
    d['timestamp'] = ts

    for key, info in site.elements['attributes'].iteritems():
    
        # print key, info
        
        # print etree.tostring(e, pretty_print=True)

        if info.has_key('path'):
            ee = e.xpath(info['path'])
            if len(ee) == 0:
                d[key] = None
                continue
        else:
            ee = [e]

        if info.has_key('function'):
            f = info['function']
            v = [f(x) for x in ee]
        elif info.has_key('attrib'):
            if info['attrib'] == 'text':
                # v = [x.text for x in ee]
                v = ee
            elif info['attrib'] == 'html':
                v = [etree.tostring(x) for x in ee]
            else:
                v = [(x.attrib[info['attrib']] if x.attrib.has_key(info['attrib']) else '') for x in ee]

        if info.has_key('regex') and v is not None:
            if type(v) == list:
                v = [re.findall(info['regex'], x)[0] if re.findall(info['regex'], x) else None for x in v]
            else:
                v = re.findall(info['regex'], v)[0] if re.findall(info['regex'], v) else None

        # print v
        d[key] = v

    dlist.append(d)

# for d in dlist:
    # print "==========================================================="
    # for k, v in d.iteritems():
        # print k, ":", v

import json
print json.dumps(dlist)