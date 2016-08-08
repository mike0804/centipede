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
    #'stop' : lambda x: True,
}

elements = {
    'path': '//*[@id="container"]/div[1]/table[1]/tr/td[contains(@class,"trow")]/..',
    'attributes': {
    
        'user_fullname'  : {
            'path'  : './td[2]/a/text()', 
            'attrib': 'text',},
            
        'user_url'  : {
            'path'  : './td[2]/a', 
            'attrib': 'href',},
            
        'uid'    : {
            'path'  : './td[2]/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
                
        'user_country' :{
            'path'  : './td[2]/img',
            'attrib': 'src',},
              
        'user_title' :{
            'path'  : './td[2]/span/text()',
            'attrib': 'text',},
            
        'user_joined' : {
            'path'  : './td[3]/text()', 
            'attrib': 'text',
            'regex' : r'\w+'},
            
        'user_number_posts' : {
            'path'  : './td[5]/text()', 
            'attrib': 'text'},
            
        'user_number_threads' : {
            'path'  : './td[6]/text()', 
            'attrib': 'text'},
            
        'user_last_visit' : {
            'path'  : './td[4]/text()', 
            'attrib': 'text'},
            
        'user_referrals' : {
            'path'  : './td[7]/text()', 
            'attrib': 'text'},
            
        
    }
}

new_jobs = [{
    'path' : '//*[@id="container"]/div[1]/table[1]/tr/td[contains(@class,"trow")]/../td[2]/a',
    'module': 'offensivecommunity_detailsusers',
    #'prefix': 'http://offensivecommunity.net/',
}]
