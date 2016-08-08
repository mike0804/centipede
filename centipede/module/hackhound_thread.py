# from lxml import html
# import requests
# import re

    
http_rules = {    
    'method'  : 'GET',
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//*[@title="Next page"]')) == 0,
    #'stop' : lambda x: True,
}

elements = {
    'path': '//*[@id="forum_table"]/tr[contains(@class,"__topic")]',
    'attributes': {
        'tid'   : {
            #'path'  : './@data-rowid', 
            'attrib': 'data-tid'},
        'title' : {
            'path'  : './td[contains(@class,"col_f_content")]/h4/a/span/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './td[contains(@class,"col_f_content")]/h4/a', 
            'attrib': 'href'},
            
        #'uid'    : {
        #    'path'  : './div/div/span[contains(@itemprop,"author")]/span[contains(@itemprop,"name")]/a', 
        #    'attrib': 'href', 
        #    'regex' : r'\d+'},
        'user_fullname'  : {
            'path'  : './td[contains(@class,"col_f_content")]/span/span[contains(@style,"color")]/text()', 
            'attrib': 'text',},
        'thread_time'  : {
            'path'  : './td[contains(@class,"col_f_content")]/span/span[contains(@itemprop,"date")]/text()', 
            'attrib': 'text',},
        'replies'  : {
            'path'  : './td[contains(@class,"col_f_views")]/ul/li[contains(text(),"repl")]/text()[1]', 
            'attrib': 'text', 
            'regex' : r'\d+'},
        'views'  : {
            'path'  : './td[contains(@class,"col_f_views")]/ul/li[contains(text(),"View")]/text()[1]', 
            'attrib': 'text', 
            'regex' : r'\d+'},
            
        'last_posts_time'  : {
            'path'  : './td[contains(@class,"col_f_post")]/ul/li/a[contains(@title,"Go to last post")]/text()', 
            'attrib': 'text',},
        'last_posts_user'  : {
            'path'  : './td[contains(@class,"col_f_post")]/ul/li/span[contains(@style,"color")]/text()', 
            'attrib': 'text',},
        #'last_posts_uid'  : {
        #    'path'  : './ul/li/a[contains(@title,"profile") and contains(@data-ipshover-target,"forums")]', 
        #    'attrib': 'href', 
        #    'regex' : r'\d+'},
    }
}

new_jobs = [{
    'path'  : '//*[@id="forum_table"]/tr[contains(@class,"__topic")]/td[contains(@class,"col_f_content")]/h4/a',
    'module': 'hackhound_question',
    #'prefix': 'http://hackhound.org/forums/',
}]