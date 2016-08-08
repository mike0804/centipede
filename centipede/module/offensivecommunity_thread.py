# from lxml import html
# import requests
# import re

    
http_rules = {    
    'method'  : 'GET',
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//*[@class="pagination_next"]')) == 0,
    # 'stop' : lambda x: True,
}

elements = {
    'path': '//*[@id="container"]/div/table/tr/td[contains(@class,"forumdisplay")]/..',
    'attributes': {
        'type_post'   : {
            'path'  : './td[1]/div/span', 
            'attrib': 'title'},
        'tid'   : {
            'path'  : './td[3]/div/span/span[contains(@id,"tid")]', 
            'attrib': 'id', 
            'regex' : r'\d+'},
        'title' : {
            'path'  : './td[3]/div/span/span[contains(@id,"tid")]/a/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './td[3]/div/span/span[contains(@id,"tid")]/a', 
            'attrib': 'href'},
            
        'uid'    : {
            'path'  : './td[3]/div/div/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'user_fullname'  : {
            'path'  : './td[3]/div/div/a/text()', 
            'attrib': 'text',},
        'replies'  : {
            'path'  : './td[4]/a/text()', 
            'attrib': 'text',},
        'views'  : {
            'path'  : './td[5]/text()', 
            'attrib': 'text',},
        'votes'  : {
            'path'  : './td[6]/ul/li[1]/text()', 
            'attrib': 'text',
            'regex' : r'([\d\.]+) out of 5'},
        'last_posts_time'  : {
            'path'  : './td[7]/span/text()', 
            'attrib': 'text',},
        'last_posts_user'  : {
            'path'  : './td[7]/span/a[2]/text()', 
            'attrib': 'text',},
        'last_posts_uid'  : {
            'path'  : './td[7]/span/a[2]', 
            'attrib': 'href', 
            'regex' : r'\d+'},
    }
}

new_jobs = [{
    'path'  : '//*[@id="container"]/div/table/tr/td[contains(@class,"forumdisplay")]/../td[3]/div/span/span[contains(@id,"tid")]/a',
    'module': 'offensivecommunity_question',
    'prefix': 'http://offensivecommunity.net/',
}]