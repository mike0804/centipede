

http_rules = {    
    'method' : 'GET',    
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//*[@id="content"]/div/div/div[3]//a[last()][contains(@class,"text")]')) == 0,
}

elements = {
    'path': '//*[@id="content"]/div/div/form[contains(@method,"post")]/ol/li[contains(@id,"post")]',
    'attributes': {
        'pid'  : {
            #'path'  : '/', 
            'attrib': 'id', 
            'regex' : r'\d+'},
        'uid'  : {
            'path'  : './div[1]/div/h3/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'username'  : {
            'path'  : './div[1]/div/h3/a/span/text()', 
            'attrib': 'text',},
        'user_title' :{
            'path'  : './div[1]/div/h3/em/text()',
            'attrib': 'text'},
        'user_posts' :{
            'path'  : './div[1]/div/div[2]/dl[2]/dd/a/text()',
            'attrib': 'text',},  
        'user_time_joined' :{
            'path'  : './div[1]/div/div[2]/dl[1]/dd/text()',
            'attrib': 'text',},
        'user_location' :{
            'path'  : './div[1]/div/div[2]/dl[3]/dd/a/text()',
            'attrib': 'text',}, 
            
        'post_number' :{
            'path'  : './div[2]/div[contains(@class,"messageMeta")]/div[2]/a/text()',
            'attrib': 'text',
            'regex' : r'\d+',},   
        'post_date' :{
            'path'  : './div[2]/div[contains(@class,"messageMeta")]/div[1]/span/a/span/text()',
            'attrib': 'text',},
        'post_date_last_edited' :{
            'path'  : './div[2]/div[contains(@class,"editDate")]/span/text()',
            'attrib': 'text',},
        'post_content'  : {
            'path'  : './div[2]/div[contains(@class,"messageContent")]', 
            'attrib': 'html',},
    }
    
}