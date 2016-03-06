from lxml import html
from lxml import etree
import requests
import re
import time
import json

debug_mode = True
log = True
log_print = True

def next_job():
    with open('jobs', 'r') as fin:
        data = fin.read().splitlines(True)

    if data:
        job = data[0]
        print "Job get: " + job
        
        splits = job.rstrip().split("\t")
        if len(splits) != 2:
            return None
        else:
            url, module = splits
            # print module
            return (url, load_module(module))
    else:
        return None

def done_job():
    with open('jobs', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('jobs', 'w') as fout:
        fout.writelines(data[1:])
    
    print "Job done: " + data[0]

def dump_jobs(tree, m):
    if hasattr(m, 'new_jobs'):

        jlist = list()
        for nj in m.new_jobs:
            el = tree.xpath(nj['path'])
            for e in el:
                url = e.attrib['href'] if not nj.has_key('prefix') else nj['prefix'] + e.attrib['href']
                j = "%s\t%s\n" % (url, nj['module'])
                jlist.append(j)

        print "Dump %d jobs" % len(jlist)

        with open('jobs', 'a+') as fout:
            fout.writelines(jlist)

    else:
        return

def dump_data(dlist, url):
    dir = 'crawl_result'
    fname = url.replace('http://', '').replace('/', '_')

    with open('./%s/%s.json' % (dir, fname), 'w') as fout:
        json.dump(dlist, fout)


def load_module(module):
    if module == "stackexchange.unix.questions":
        import centipede.stackexchange.unix.questions
        m    = centipede.stackexchange.unix.questions
    elif module == "stackexchange.unix.qna":
        import centipede.stackexchange.unix.qna
        m    = centipede.stackexchange.unix.qna
    elif module == "linuxquestions.list":
        import centipede.linuxquestions.list
        m    = centipede.linuxquestions.list
    elif module == "linuxquestions.thread":
        import centipede.linuxquestions.thread
        m    = centipede.linuxquestions.thread
    else:
        assert False, "Module undefined."

    return m

job = next_job()

while (job):
    url, m = job

    crawl_rules = m.http_rules
    dlist = list()

    params  = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    if crawl_rules.has_key('page'):
        params[crawl_rules['page']['key']] = int(crawl_rules['page']['value'])

    if crawl_rules.has_key('pagesize'):
        params[crawl_rules['pagesize']['key']] = crawl_rules['pagesize']['value']

    if crawl_rules.has_key('params'):
        for k, v in crawl_rules['params'].iteritems():
            params[k] = v

    stop = False

    while (not stop):

        r    = requests.get(url, params=params, headers=headers)
        print r.url
        tree = html.fromstring(r.content)

        elements = tree.xpath(m.elements['path'])

        print len(elements)
        # Quicknote: xpath always return a "list" of elements no matter how many items
        #            are matched

        # print m.elements['path']
        # print elements

        ts = time.time()

        for e in elements:
            d = {}
            d['timestamp'] = ts

            for key, info in m.elements['attributes'].iteritems():

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


        # Dump new jobs if it is defined
        dump_jobs(tree, m)

        # If page is defined, increase one. Continue until stop condition is matched
        if crawl_rules.has_key('page'):
            params[crawl_rules['page']['key']] += 1

        # Stop condition must be a function, stop if not defined.
        if crawl_rules.has_key('stop'):
            f = crawl_rules['stop']
            if not hasattr(f, '__call__'):
                assert False, "Stop condition must be a function."
            stop = f(tree)
        else:
            stop = True

        time.sleep(5)

    print "Dump data."
    dump_data(dlist, url)
    
    done_job()
    job = next_job()




















