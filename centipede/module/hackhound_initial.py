# from lxml import html
# import requests
# import re

    
http_rules = {    
    'method'  : 'GET',
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    #'stop' : lambda x: len(x.xpath('//*[@class="pagination_next"]')) == 0,
     'stop' : lambda x: True,
}

elements = {
    'path': '//*[contains(@summary,"Forums within the category")]/tr/td[@class="col_c_forum"]/..',
    'attributes': {
        'fid'   : {
            'path'  : './td[@class="col_c_forum"]/h4/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'title' : {
            'path'  : './td[@class="col_c_forum"]/h4/a/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './td[@class="col_c_forum"]/h4/a', 
            'attrib': 'href'},
        'description' : {
            'path'  : './td[@class="col_c_forum"]/p/text()', 
            'attrib': 'text'},
        'title_subforum' : {
            'function': lambda e: e.xpath('./td[@class="col_c_forum"]/ol/li/a/text()')},
        'url_subforum' : {
            'function': lambda e: [ee.attrib['href'] for ee in e.xpath('./td[@class="col_c_forum"]/ol/li/a')]},
            
         
        'number_of_topics'  : {
            'path'  : './td[contains(@class,"col_c_stats")]/ul/li[contains(text(),"topics")]/strong/text()', 
            'attrib': 'text'},
        'number_of_replies'  : {
            'path'  : './td[contains(@class,"col_c_stats")]/ul/li[contains(text(),"replies")]/strong/text()', 
            'attrib': 'text'},
            
            
        'last_thread_title'  : {
            'path'  : './td[contains(@class,"col_c_post")]/ul/li/a[@hovercard-ref="topicPreview"][1]/text()', 
            'attrib': 'text'},
        'last_subforum_title'  : {
            'path'  : './td[contains(@class,"col_c_post")]/ul/li/a[@hovercard-ref="topicPreview"][2]/text()', 
            'attrib': 'text'},
        'last_posts_time'  : {
            'path'  : './td[contains(@class,"col_c_post")]/ul/li/a[@title="View last post"]/text()', 
            'attrib': 'text'},
        'last_posts_user'  : {
            'path'  : './td[contains(@class,"col_c_post")]/ul/li/span/text()', 
            'attrib': 'text',},
        'last_posts_url'  : {
            'path'  : './td[contains(@class,"col_c_post")]/ul/li/a[@title="View last post"]', 
            'attrib': 'href'},
    }
}

new_jobs = [
{
    'path'  : '//*[contains(@summary,"Forums within the category")]/tr/td[@class="col_c_forum"]/../td[contains(@class,"col_c_forum")]/h4/a',
    'module': 'hackhound_thread',
    #'prefix': 'http://hackhound.org/forums/',
},
{
    'path'  : '//*[contains(@summary,"Forums within the category")]/tr/td[@class="col_c_forum"]/../td[contains(@class,"col_c_forum")]/ol/li/a',
    'module': 'hackhound_thread',
    #'prefix': 'http://hackhound.org/forums/',
}]