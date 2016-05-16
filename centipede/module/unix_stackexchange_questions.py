# from lxml import html
# import requests
# import re

# cookies = dict(unixuser="t=&s=&p=[2|2][10|50]")
# params = {'sort': 'newest', 'pagesize': '50', 'page': '1'}
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# r = requests.get('http://unix.stackexchange.com/questions/tagged/security', params=params, headers=headers)


# with open('test.html', 'rb') as fp:
    # tree = html.fromstring(fp.read())


# url = "http://unix.stackexchange.com/questions/tagged/security"
    
http_rules = {    
    'method'  : 'GET',    
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//div[@id="questions"]/div')) == 0,
    # 'stop' : lambda x: True,
    
    'params' : {
        'sorted': 'newest',
        'pagesize': 50,
    }
}

elements = {
    'path': '//div[@id="questions"]/div[@class="question-summary"]',
    'attributes': {
        'tid'   : {
            # 'path'  : './/', 
            'attrib': 'id', 
            'regex' : r'\d+'},
        'title' : {
            'path'  : './div[2]/h3/a/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './div[2]/h3/a', 
            'attrib': 'href'},
        'time'  : {
            'path'  : './div[2]/div[3]/div/div[1]/span', 
            'attrib': 'title'},
            
        'uid'    : {
            'path'  : './div[2]/div[3]/div/div[3]/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'username': {
            'path'  : './div[2]/div[3]/div/div[3]/a', 
            'attrib': 'href', 
            'regex' : r'[\w_-]+$'},
        'user_fullname'  : {
            'path'  : './div[2]/div[3]/div/div[3]/a/text()', 
            'attrib': 'text',},
        'user_rep'  : {
            'path'  : './div[2]/div[3]/div/div[3]/div/span[1]/text()', 
            'attrib': 'text',},

        'vote'  : {
            'path'  : './div[1]/div[2]/div[1]/div/span/strong/text()', 
            'attrib': 'text',},
        'answer': {
            'path'  : './div[1]/div[2]/div[2]/strong/text()', 
            'attrib': 'text',},
        'answer_status': {
            'path'  : './div[1]/div[2]/div[2]', 
            'attrib': 'class', 
            'regex' : r'(unanswered|answered|answered-accepted)$'},
        'views'     : {
            'path'  : './div[1]/div[3]', 
            'attrib': 'title',
            'regex' : r'[\d,]+'},
            
        'tags'      : {
            # 'path'  : '//div[@id="questions"]/div', 
            'function': lambda e: e.xpath('./div[2]/div[2]/a/text()'),},
    }
}

new_jobs = [{
    'path'  : '//div[@id="questions"]/div[@class="question-summary"]/div[2]/h3/a',
    'module': 'unix_stackexchange_qna',
    'prefix': 'http://unix.stackexchange.com',
}]