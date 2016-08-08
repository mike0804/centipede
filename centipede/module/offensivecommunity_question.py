

http_rules = {    
    'method' : 'GET',    
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//*[@class="pagination_next"]')) == 0,
}

elements = {
    'path': '//*[@id="container"]/div/table/tr[2]/td/div/div[contains(@class,"post")]',
    'attributes': {
        'pid'  : {
            #'path'  : '/', 
            'attrib': 'id', 
            'regex' : r'\d+'},
        'uid'  : {
            'path'  : './div[1]/div[2]/strong/span/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'username'  : {
            'path'  : './div[1]/div[2]/strong/span/a/text()', 
            'attrib': 'text',},
        'user_experience' :{
            'path'  : './div[1]/div[2]/span/text()[1]',
            'attrib': 'text'},
        'user_posts' :{
            'path'  : './div[1]/div[3]/text()[1]',
            'attrib': 'text',
            'regex' : r'Posts: (\d+)',}, 
        'user_threads' :{
            'path'  : './div[1]/div[3]/text()[2]',
            'attrib': 'text',
            'regex' : r'Threads: (\d+)',},    
        'user_time_joined' :{
            'path'  : './div[1]/div[3]/text()[3]',
            'attrib': 'text',
            #'regex' : r'Joined: ([A-Za-z]+\d+)',},
            'regex' : r'Joined: (.+)',},  
        'user_reputation' :{
            'path'  : './div[1]/div[3]/a/strong/text()',
            'attrib': 'text',}, 
        'user_location' :{
            'path'  : './div[1]/div[3]/text()[6]',
            'attrib': 'text',
            'regex' : r'Location: (.+)',},    
        'user_country' :{
            'path'  : './div[1]/div[3]/img',
            'attrib': 'src',
            },
        'user_money'  : {
            'path'  : './div[1]/div[3]/span/a/text()', 
            'attrib': 'text', 
            'regex' : r'([0-9.,]+)'},  
             
             
             
             
        'post_number' :{
            'path'  : './div[2]/div[1]/div/strong/a/text()',
            'attrib': 'text',
            'regex' : r'\d+',},   
        'post_date' :{
            'path'  : './div[2]/div[1]/span/text()',
            'attrib': 'text',},
        'post_content'  : {
            'path'  : './div[2]/div[contains(@class,"post_body")]', 
            'attrib': 'html',}, 
            
    }
}