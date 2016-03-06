

http_rules = {    
    'method' : 'GET',    
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//a[@rel="next"]')) == 0,
}

elements = {
    'path': '//*[@id="posts"]/div[not(@id="lastpost")]',
    'attributes': {
        
        # thread_title_4175546925
        'time'   : {
            'path'  : './div/div/div/table/tr[1]/td[1]/text()[3]',
            'attrib': 'text',}, 
        'floor' : {
            'path'  : './div/div/div/table/tr[1]/td[2]/a[last()]/strong/text()', 
            'attrib': 'text'},
        # 'url' : {
            # 'path'  : './td[3]/div[1]/a[last()]', 
            # 'attrib': 'href'},
        
        # /questions/user/malwaremustdie-895658/
        'username'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[1]/div/text()[2]', 
            'attrib': 'text',}, 
        'user_member_type'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[2]/text()', 
            'attrib': 'text',}, 
        'user_is_contribution_member'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[3]/a/text()', 
            'attrib': 'text'},
        'uid'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[last()]/div[last()-1]/span', 
            'attrib': 'id',
            'regex' : r'repdisplay_\d+_(\d+)$',},
        
        'user_location'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[last()]', 
            'attrib': 'html',
            'regex' : r'Location: (.+)\<\/div\>',},
        'user_registeredAt'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[last()]', 
            'attrib': 'html',
            'regex' : r'Registered: (.+)\<\/div\>',},
        'user_distribution'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[last()]', 
            'attrib': 'html',
            'regex' : r'Distribution: (.+)\<\/div\>',},
        'user_rep'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[last()]/div[last()-1]/span/node()[last()]', 
            'attrib': 'html',
            'regex' : r'\<smallfont\>\((\d+)\)\<\/smallfont\>',},
        'user_blog_entries'  : {
            'path'  : './div/div/div/table/tr[2]/td[1]/div[last()]/div/a/text()', 
            'attrib': 'text'},
        
        
        'content'  : {
            'path'  : './div/div/div/table/tr[2]/td[2]/div[last()]', 
            'attrib': 'html',},
        'pid'  : {
            'path'  : './div/div/div', 
            'attrib': 'id',
            'regex' : r'edit(\d+)',},
    }
}