# from lxml import html
# import requests
# import re

    
http_rules = {    
    'method'  : 'GET',
}

elements = {
    'path': '//*[@id="page-body"]/div/div/ul/li/dl/dt/a[contains(@class,"forumtitle")]/../..',
    'attributes': {
        'fid'   : {
            'path'  : './dt/a[contains(@class,"forumtitle")]', 
            'attrib': 'href', 
            'regex' : r'f=([\d\.]+)&sid'},
        'title' : {
            'path'  : './dt/a[contains(@class,"forumtitle")]/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './dt/a[contains(@class,"forumtitle")]', 
            'attrib': 'href'},
        'description' : {
            'path'  : './dt/a[contains(@class,"forumtitle")]/../text()', 
            'attrib': 'text'},
        'title_subforum' : {
            'function': lambda e: e.xpath('./dt/a[contains(@class,"forumtitle")]/../a[contains(@class,"subforum")]/text()')},
        'url_subforum' : {
            'function': lambda e: [ee.attrib['href'] for ee in e.xpath('./dt/a[contains(@class,"forumtitle")]/../a[contains(@class,"subforum")]')]},
            
            
        'number_of_topics'  : {
            'path'  : './dd[contains(@class,"topics")]/text()', 
            'attrib': 'text'},
        'number_of_posts'  : {
            'path'  : './dd[contains(@class,"posts")]/text()', 
            'attrib': 'text'},
            
            
        
        'last_posts_url'  : {
            'path'  : './dd[contains(@class,"lastpost")]/span/a[contains(@href,"viewtopic")]', 
            'attrib': 'href',},
        'last_thread_id'  : {
            'path'  : './dd[contains(@class,"lastpost")]/span/a[contains(@href,"viewtopic")]', 
            'attrib': 'href', 
            'regex' : r'f=([\d\.]+)&p'},
        'last_posts_time'  : {
            'path'  : './dd[contains(@class,"lastpost")]/span/text()[5]', 
            'attrib': 'text',},
        'last_posts_user'  : {
            'path'  : './dd[contains(@class,"lastpost")]/span/a[contains(@href,"member")]/text()', 
            'attrib': 'text',},
        'last_posts_uid'  : {
            'path'  : './dd[contains(@class,"lastpost")]/span/a[contains(@href,"member")]', 
            'attrib': 'href', 
            'regex' : r'u=([\d\.]+)&sid'},
    }
}

new_jobs = [
{
    'path'  : '//*[@id="page-body"]/div/div/ul/li/dl/dt/a[contains(@class,"forumtitle")]/../../dt/a[contains(@class,"forumtitle")]',
    'module': 'hackthissite_thread',
    'prefix': 'http://www.hackthissite.org/forums/',
},
{
    'path'  : '//*[@id="page-body"]/div/div/ul/li/dl/dt/a[contains(@class,"forumtitle")]/../../dt/a[contains(@class,"forumtitle")]/../a[contains(@class,"subforum")]',
    'module': 'hackthissite_thread',
    'prefix': 'http://www.hackthissite.org/forums/',
}]
