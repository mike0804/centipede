# from lxml import html
# import requests
# import re

    
http_rules = {    
    'method'  : 'GET',
    'page' : {
        'key'   : 'start',
        'value' : 0,
        'increment' : 25,
    },
    
    'stop' : lambda x: len(x.xpath('//*[@class="display-options"]/a[contains(text(),"Next")]')) == 0,
    # 'stop' : lambda x: True,
}

elements = {
    'path': '//*[@class="topiclist topics"]/li',
    'attributes': {
        'tid'   : {
            'path'  : './dl/dt/a[contains(@class,"topictitle")]', 
            'attrib': 'href', 
            'regex' : r't=([\d\.]+)&sid'},
        'title' : {
            'path'  : './dl/dt/a[contains(@class,"topictitle")]/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './dl/dt/a[contains(@class,"topictitle")]', 
            'attrib': 'href'},
        'time_created' : {
            'path'  : './dl/dt/a[contains(@class,"topictitle")]/../text()[last()]', 
            'attrib': 'text'},
            
        'uid'    : {
            'path'  : './dl/dt/a[contains(@class,"topictitle")]/../a[contains(@href,"memberlist")]', 
            'attrib': 'href', 
            'regex' : r'u=([\d\.]+)&sid'},
        'user_fullname'  : {
            'path'  : './dl/dt/a[contains(@class,"topictitle")]/../a[contains(@href,"memberlist")]/text()', 
            'attrib': 'text',},
        'replies'  : {
            'path'  : './dl/dd[contains(@class,"posts")]/text()', 
            'attrib': 'text',},
        'views'  : {
            'path'  : './dl/dd[contains(@class,"views")]/text()', 
            'attrib': 'text',},
        'last_posts_time'  : {
            'path'  : './dl/dd[contains(@class,"lastpost")]/span/text()[last()]', 
            'attrib': 'text',},
        'last_posts_user'  : {
            'path'  : './dl/dd[contains(@class,"lastpost")]/span/a[contains(@href,"member")]/text()', 
            'attrib': 'text',},
        'last_posts_uid'  : {
            'path'  : './dl/dd[contains(@class,"lastpost")]/span/a[contains(@href,"member")]', 
            'attrib': 'href', 
            'regex' : r'u=([\d\.]+)&sid'},
        'last_posts_url'  : {
            'path'  : './dl/dd[contains(@class,"lastpost")]/span/a[contains(@href,"topic")]', 
            'attrib': 'href'},
    }
}

new_jobs = [{
    'path'  : '//*[@class="topiclist topics"]/li/dl/dt/a[contains(@class,"topictitle")]',
    'module': 'hackthissite_question',
    'prefix': 'http://www.hackthissite.org/forums/',
}]
