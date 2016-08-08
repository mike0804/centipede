# from lxml import html
# import requests
# import re

    
http_rules = {    
    'method'  : 'GET',
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//*[@id="content"]/div/div/div[3]//a[last()][contains(@class,"text")]')) == 0,
    # 'stop' : lambda x: True,
}

elements = {
    'path': '//*[@id="content"]/div/div/div[4]/form/ol/li[contains(@id,"thread")]',
    'attributes': {
        'tid'   : {
            #'path'  : './td[3]/div/span/span', 
            'attrib': 'id', 
            'regex' : r'\d+'},
        'locked' : {
            'path'  : './div[2]/div/div[contains(@class,"iconKey")]/span[contains(@class,"locked")]', 
            'attrib': 'title'},
        'sticky' : {
            'path'  : './div[2]/div/div[contains(@class,"iconKey")]/span[contains(@class,"sticky")]', 
            'attrib': 'title'},
        'title' : {
            'path'  : './div[2]/div/h3/a/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './div[2]/div/h3/a', 
            'attrib': 'href'},
           
             
        'uid'    : {
            'path'  : './div[2]/div/div[contains(@class,"second")]/div[1]/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'user_fullname'  : {
            'path'  : './div[2]/div/div[contains(@class,"second")]/div[1]/a/text()', 
            'attrib': 'text',},
        'thread_time'  : {
            'path'  : './div[2]/div/div[2]/div[1]/span/a/span/text()', 
            'attrib': 'text',},
        'replies'  : {
            'path'  : './div[3]/dl[1]/dd/text()', 
            'attrib': 'text',},
        'views'  : {
            'path'  : './div[3]/dl[2]/dd/text()', 
            'attrib': 'text',},
            
            
        'last_posts_time'  : {
            'path'  : './div[4]/dl/dd/a/span/text()', 
            'attrib': 'text',},
        'last_posts_user'  : {
            'path'  : './div[4]/dl/dt/a/text()', 
            'attrib': 'text',},
        'last_posts_uid'  : {
            'path'  : './div[4]/dl/dt/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
    }
}

new_jobs = [{
    'path' : '//*[@id="content"]/div/div/div[4]/form/ol/li[contains(@id,"thread")]/div[2]/div/h3/a',
    'module': 'wildersecurity_questions',
    'prefix': 'http://www.wilderssecurity.com/',
}]
