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
    'path': '//*[@id="content"]/table/tbody/tr/td/table/tr[contains(@class,"forumstyle")]',
    'attributes': {
        'fid'   : {
            'path'  : './td[2]/strong/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'title' : {
            'path'  : './td[2]/strong/a/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './td[2]/strong/a', 
            'attrib': 'href'},
        'uid_moderate' : {
            'path'  : './td[2]/div/a[contains(@href,"member")]', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'title_subforum' : {
            'function': lambda e: e.xpath('./td[2]/div/ul/li/a/text()')},
        'url_subforum' : {
            'function': lambda e: [ee.attrib['href'] for ee in e.xpath('./td[2]/div/ul/li/a')]},
            
            
        'number_of_threads'  : {
            'path'  : './td[3]/span/text()', 
            'attrib': 'text', 
            'regex' : r'\d+'},
        'number_of_posts'  : {
            'path'  : './td[4]/span/text()', 
            'attrib': 'text', 
            'regex' : r'\d+'},
            
            
        
        'last_posts_title'  : {
            'path'  : './td[5]/span/a[1]/strong/text()', 
            'attrib': 'text',},
        'last_posts_url'  : {
            'path'  : './td[5]/span/a[1]', 
            'attrib': 'href',},
        'last_thread_id'  : {
            'path'  : './td[5]/span/a[1]', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'last_posts_time'  : {
            'path'  : './td[5]/span/text()', 
            'attrib': 'text',},
        'last_posts_user'  : {
            'path'  : './td[5]/span/a[2]/text()', 
            'attrib': 'text',},
        'last_posts_uid'  : {
            'path'  : './td[5]/span/a[2]', 
            'attrib': 'href', 
            'regex' : r'\d+'},
    }
}

new_jobs = [
{
    'path'  : '//*[@id="content"]/table/tbody/tr/td/table//tr[contains(@class,"forumstyle")]/td[2]/strong/a',
    'module': 'offensivecommunity_thread',
    'prefix': 'http://offensivecommunity.net/',
},
{
    'path'  : '//*[@id="content"]/table/tbody/tr/td/table/tr[contains(@class,"forumstyle")]/td[2]/div/ul/li/a',
    'module': 'offensivecommunity_thread',
    'prefix': 'http://offensivecommunity.net/',
}]