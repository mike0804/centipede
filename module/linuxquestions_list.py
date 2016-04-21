

http_rules = {    
    'method' : 'GET',    
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//a[@rel="next"]')) == 0,
}

elements = {
    'path': '//*[@id="threadbits_forum_4"]/tr',
    'attributes': {
        
        # thread_title_4175546925
        'tid'   : {
            'path'  : './td[3]/div[1]/a[last()]',
            'attrib': 'id', 
            'regex' : r'(\d+)$'}, 
        'title' : {
            'path'  : './td[3]/div[1]/a[last()]/text()', 
            'attrib': 'text'},
        'url' : {
            'path'  : './td[3]/div[1]/a[last()]', 
            'attrib': 'href'},
        
        # /questions/user/malwaremustdie-895658/
        'lastpost_uid'  : {
            'path'  : './td[4]/div/a[1]', 
            'attrib': 'href',
            'regex' : r'-(\d+)\/$'}, 
        'lastpost_username'  : {
            'path'  : './td[4]/div/a[1]', 
            'attrib': 'href',
            'regex' : r'\/([\w_-]+)-\d+\/$'}, 
        'lastpost_user_fullname'  : {
            'path'  : './td[4]/div/a[1]/text()', 
            'attrib': 'text'},
        
        'lastpost_date'  : {
            'path'  : './td[4]/div/text()[1]', 
            'attrib': 'text'},
        'lastpost_time'  : {
            'path'  : './td[4]/div/span/text()', 
            'attrib': 'text'},
            
        # window.open('/questions/user/malwaremustdie-895658/', '_self')
        'uid'    : {
            'path'  : './td[3]/div[2]/span', 
            'attrib': 'onclick', 
            'regex' : r'-(\d+)\/'},
        'username': {
            'path'  : './td[3]/div[2]/span', 
            'attrib': 'onclick', 
            'regex' : r'\/([\w_-]+)-\d+\/'},
        'user_fullname'  : {
            'path'  : './td[3]/div[2]/span/text()', 
            'attrib': 'text',},

        'replies'  : {
            'path'  : './td[5]/a/text()', 
            'attrib': 'text',},
        'views'     : {
            'path'  : './td[6]/text()', 
            'attrib': 'text',},
        
        # https://lqo-thequestionsnetw.netdna-ssl.com/questions/images/statusicon/thread_hot.gif
        'icon1'     : {
            'path'  : './td[1]/img',
            'attrib': 'src', 
            'regex' : r'\/thread_([\w_-]+)\.gif$'},
        'icon2'     : {
            'path'  : './td[2]/img',
            'attrib': 'alt',},
        
        'sticky'    : {
            'path'  : './td[3]/div[1]/span[1]/img[contains(@src, "sticky")]',
            'attrib': 'alt',},
        'tags'    : {
            'path'  : './td[3]/div[1]/span[1]/img[contains(@src, "tag")]',
            'attrib': 'alt',},
        
        # 'tags'      : {
            # 'function': lambda e: e.xpath('./div[2]/div[2]/a/text()'),},
    }
}

new_jobs = [{
    'path'  : '//*[@id="threadbits_forum_4"]/tr/td[3]/div[1]/a[last()]',
    'module': 'linuxquestions_thread',
    'prefix': 'http://www.linuxquestions.org',
}]