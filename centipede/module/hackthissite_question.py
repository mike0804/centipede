

http_rules = {    
    'method' : 'GET',    
    'page' : {
        'key'   : 'start',
        'value' : 0,
        'increment' :10,
    },
    
    #'stop' : lambda x: len(x.xpath('//*[@class="display-options"]/a[contains(text(),"Next")]')) == 0,
}

elements = {
    'path': '//*[contains(@class,"post bg")]',
    'attributes': {
        'pid'  : {
            'path'  : './div/div[contains(@class,"postbody")]/h3/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'uid'  : {
            'path'  : './div/dl[contains(@class,"postprofile")]/dt/a[contains(@href,"memberlist")]', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'username'  : {
            'path'  : './div/dl[contains(@class,"postprofile")]/dt/a[contains(@href,"memberlist")]/text()', 
            'attrib': 'text',},
        'user_title' :{
            'path'  : './div/dl[contains(@class,"postprofile")]/dd/img[contains(@src,"ranks")]/../text()',
            'attrib': 'text'},
        'user_posts' :{
            'path'  : './div/dl[contains(@class,"postprofile")]/dd/strong[contains(text(),"Posts:")]/../text()',
            'attrib': 'text',},   
        'user_time_joined' :{
            'path'  : './div/dl[contains(@class,"postprofile")]/dd/strong[contains(text(),"Joined:")]/../text()',
            'attrib': 'text'},  
        'user_url_blog' :{
            'path'  : './div/dl[contains(@class,"postprofile")]/dd/strong[contains(text(),"Blog:")]/../a',
            'attrib': 'href',}, 
        'user_signature' :{
            'path'  : './div/div[contains(@class,"postbody")]/div[contains(@class,"signature")]/text()',
            'attrib': 'text',},  
        'user_signature2' :{
            'path'  : './div/div[contains(@class,"postbody")]/div[contains(@class,"signature")]/span/text()',
            'attrib': 'text',},
             
             
             
        
        'post_title'  : {
            'path'  : './div/div[contains(@class,"postbody")]/h3/a/text()', 
            'attrib': 'text'},   
        'post_date' :{
            'path'  : './div/div[contains(@class,"postbody")]/p[contains(@class,"author")]/text()[last()-1]',
            'attrib': 'text',},
        'post_content'  : {
            'path'  : './div/div[contains(@class,"postbody")]/div[contains(@class,"content")]', 
            'attrib': 'html',},   
            
    }
}
