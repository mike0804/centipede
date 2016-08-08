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
    
    'stop' : lambda x: len(x.xpath('//*[contains(@class,"pagination")]/span/strong[contains(text(),"2771")]')) == 2,
    # 'stop' : lambda x: True,
}

elements = {
    'path': '//*[contains(@id,"memberlist")]/tbody/tr',
    'attributes': {
    
        'user_fullname'  : {
            'path'  : './td/span[contains(@class,"rank")]/../a[contains(@href,"member")]/text()', 
            'attrib': 'text',},
            
        'user_url'  : {
            'path'  : './td/span[contains(@class,"rank")]/../a[contains(@href,"member")]', 
            'attrib': 'href',},
            
        'uid'    : {
            'path'  : './td/span[contains(@class,"rank")]/../a[contains(@href,"member")]', 
            'attrib': 'href', 
            'regex' : r'u=([\d\.]+)&sid'},
              
        'user_title' :{
            'path'  : './td/span[contains(@class,"rank")]/img',
            'attrib': 'title',},
            
        'user_joined' : {
            'path'  : './td[last()]/text()', 
            'attrib': 'text'},
            
        'user_number_posts' : {
            'path'  : './td/a[contains(@title,"Search user")]/text()', 
            'attrib': 'text'},
            
        'user_website_location' : {
            'path'  : './td[@class="info"]/div/text()', 
            'attrib': 'text'},
            
        'user_website_location2' : {
            'path'  : './td[@class="info"]/div/a/text()', 
            'attrib': 'text'},
            
        
    }
}

new_jobs = [{
    'path' : '//*[contains(@id,"memberlist")]/tbody/tr/td/span[contains(@class,"rank")]/../a[contains(@href,"member")]',
    'module': 'hackthisside_detailsusers',
    'prefix': 'http://www.hackthissite.org/forums/',
}]
