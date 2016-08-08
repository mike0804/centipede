from lxml import etree
import re

def extract_comments(node):
    elements = node.xpath('./tr/td[contains(@class,"reputation")]')
    
    clist = list()

    for e in elements:
        c = {
            'vote_uid': '',
            'vote_user_fullname': '',
            'vote_lastupdate_givefor_thread': '',
            'vote_type': '',
            'vote_comment': '',
        }
        
        ee = e.xpath('./a[contains(@href,"user")]')
        if ee:
            if ee[0].attrib.has_key('href'):
                c['vote_uid'] = re.findall(r'\d+', ee[0].attrib['href'])[0]
                c['vote_user_fullname'] = ee[0].text
                
        ee = e.xpath('./a[contains(@href,"user")]/span/text()')
        if ee:
            c['vote_user_fullname'] = ee[0]
            
        ee = e.xpath('./span/text()')
        if ee:
            c['vote_lastupdate_givefor_thread'] = ee[0]   
            
        ee = e.xpath('./strong/text()')
        if ee:
            c['vote_type'] = ee[0]  
            
        ee = e.xpath('./text()[last()]')
        if ee:
            c['vote_comment'] = ee[0]  
            

        clist.append(c)

    return clist


http_rules = {
    # 'stop': lambda x: True,
    'method': 'GET',  
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//*[@class="pagination_next"]')) == 0,
}


elements = {
    'path': '//*[@id="container"]/div/table',

    'attributes': {

        'user_fullname'   : {
            'path'  : './tr/td/table/tr/td/span/strong[contains(text(),"Reputation")]/../../span[1]/strong/text()',
            'attrib': 'text',},
        'user_title'   : {
            'path'  : './tr/td/table/tr/td/span/strong[contains(text(),"Reputation")]/../../span[2]/text()',
            'attrib': 'text',},
        'user_reputation': {
            'path'  : './tr/td/table/tr/td/span/strong[contains(text(),"Reputation")]/../../span[2]/span[1]/text()',
            'attrib': 'text',},
        'user_reputation_members': {
            'path'  : './tr/td/table/tr/td/span/strong[contains(text(),"Reputation")]/../../span[2]/strong[contains(text(),"Reputation") and contains(text(),"Members")]/text()',
            'attrib': 'text',},
        'user_reputation_posts': {
            'path'  : './tr/td/table/tr/td/span/strong[contains(text(),"Reputation")]/../../span[2]/strong[contains(text(),"Reputation") and contains(text(),"Posts")]/text()',
            'attrib': 'text',},

        'votes_order' : {
            'path'  : './tr/td/table/tr/td/table/tr/td/span[contains(@class,"reputation")]/text()',
            'attrib': 'text'},
        'votes_lastweek'  : {
            'path'  : './tr/td/table/tr/td/table/tr/td/span[contains(text(),"Last week")]/../../td/span/text()',
            'attrib': 'text'},
        'votes_lastmonth'      : {
            'path'  : './tr/td/table/tr/td/table/tr/td/span[contains(text(),"Last month")]/../../td/span/text()',
            'attrib': 'text',},
        'votes_last6months'    : {
            'path'  : './tr/td/table/tr/td/table/tr/td/span[contains(text(),"Last 6")]/../../td/span/text()',
            'attrib': 'text',},
        'votes_alltime': {
            'path'  : './tr/td/table/tr/td/table/tr/td/span[contains(text(),"All Time")]/../../td/span/text()',
            'attrib': 'text'},
            
        'comments'  : {
            'function': extract_comments,},

    }
}
