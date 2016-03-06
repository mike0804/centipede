from lxml import etree
import re

def extract_comments(node):
    elements = node.xpath('./table/tr[last()]/td[2]/div/table/tbody/tr[contains(@class, "comment")]')
    
    clist = list()

    for e in elements:
        c = {
            'vote': '',
            'content': '',
            'commentor_id': '',
            'commentor_username': '',
            'commentor_full_name': '',
            'commentor_rep': '',
        }
        
        ee = e.xpath('./td[1]//span/text()')
        if ee:
            c['vote'] = ee[0]
        
        ee = e.xpath('./td[2]/div/span[1]')
        if ee:
            c['content'] = etree.tostring(ee[0])
        
        ee = e.xpath('./td[2]/div/a[last()]')
        if ee:
            if ee[0].attrib.has_key('href'):
                c['commentor_id'] = re.findall(r'\d+', ee[0].attrib['href'])[0]
                c['commentor_username'] = re.findall(r'[\w_-]+$', ee[0].attrib['href'])[0]
                c['commentor_full_name'] = ee[0].text
            if ee[0].attrib.has_key('title'):
                c['commentor_rep'] = re.findall(r'\d+', ee[0].attrib['title'])[0]

        clist.append(c)

    return clist


http_rules = {
    # 'stop': lambda x: True,
    'method': 'GET',
}


elements = {
    'path': '//div[@id="question" or contains(@id, "answer-")]',

    'attributes': {


        'qid'   : {
            # 'path'  : './/',
            'attrib': 'data-questionid',},
        'aid'   : {
            # 'path'  : './/',
            'attrib': 'data-answerid',},
        'type': {
            # 'path'  : './/',
            'attrib': 'class',
            'regex' : r'(question|accepted-answer|answer)$'},

        'votes' : {
            'path'  : './table/tr[1]/td[1]/div/span[1]/text()',
            'attrib': 'text'},
        'content'  : {
            'path'  : './table/tr[1]/td[2]//div[@class="post-text"]',
            'attrib': 'html'},
        'tags'      : {
            'path'  : './table/tr[1]/td[2]/div/div[2]/a/text()',
            'attrib': 'text',},

        'post_time'    : {
            'path'  : './table/tr[1]/td[2]//table/tr/td[last()]/div/div[1]/span',
            'attrib': 'title',},
        'post_uid': {
            'path'  : './table/tr[1]/td[2]//table/tr/td[last()]/div/div[3]/a',
            'attrib': 'href',
            'regex' : r'\d+'},
        'post_username': {
            'path'  : './table/tr[1]/td[2]//table/tr/td[last()]/div/div[3]/a',
            'attrib': 'href',
            'regex' : r'[\w_-]+$'},
        'post_user_fullname'  : {
            'path'  : './table/tr[1]/td[2]//table/tr/td[last()]/div/div[3]/a/text()',
            'attrib': 'text',},
        'post_rep'  : {
            'path'  : './table/tr[1]/td[2]//table/tr/td[last()]/div/div[3]/div/span[1]/text()',
            'attrib': 'text',},

        'edit_time'    : {
            'path'  : './table/tr[1]/td[2]//table/tr/td[position() = 2]/div/div[1]//span',
            'attrib': 'title',},
        'edit_uid': {
            'path'  : './table/tr[1]/td[2]//table/tr/td[position() = 2]/div/div[3]/a',
            'attrib': 'href',
            'regex' : r'\d+'},
        'edit_username': {
            'path'  : './table/tr[1]/td[2]//table/tr/td[position() = 2]/div/div[3]/a',
            'attrib': 'href',
            'regex' : r'[\w_-]+$'},
        'edit_user_fullname'  : {
            'path'  : './table/tr[1]/td[2]//table/tr/td[position() = 2]/div/div[3]/a/text()',
            'attrib': 'text',},
        'edit_rep'  : {
            'path'  : './table/tr[1]/td[2]//table/tr/td[position() = 2]/div/div[3]/div/span[1]/text()',
            'attrib': 'text',},

        'comments'  : {
            'function': extract_comments,},

    }
}
