

http_rules = {    
    'method' : 'GET',    
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: len(x.xpath('//*[contains(@title,"Next page")]')) == 0,
    # 'stop' : lambda x: True,
}

elements = {
    'path': '//*[contains(@class,"post_block hentry")]',
    'attributes': {
        'pid'  : {
            #'path'  : './div/div/div/a', 
            'attrib': 'id', 
            'regex' : r'\d+'},
        #'uid'  : {
        #    'path'  : './div/div/div/article/aside/h3[contains(@itemprop,"creator")]/strong/a', 
        #    'attrib': 'href', 
        #    'regex' : r'profile/(\d+)-'},
        'username'  : {
            'path'  : './div/h3/span[contains(@itemprop,"creator name")]/span/text()', 
            'attrib': 'text',},
        'number_post' :{
            'path'  : './div/h3/span/a/text()[1]',
            'attrib': 'text',
            'regex' : r'\d+'},
        'user_posts' :{
            'path'  : './div/div[@class="author_info"]/div/ul[@class="basic_info"]/li[contains(@class,"post_count")]/text()',
            'attrib': 'text',
            'regex' : r'\d+'},
        'user_group_title' :{
            'path'  : './div/div[@class="author_info"]/div/ul[@class="basic_info"]/li[contains(@class,"group_title")]/span/text()',
            'attrib': 'text'}, 
        'user_location' :{
            'path'  : './div/div[@class="author_info"]/div/ul[@class="custom_fields"]/li/span[contains(text(),"Location")]/../span[2]/text()',
            'attrib': 'text'},
        'user_title' :{
            'path'  : './div/div[@class="author_info"]/div/ul[@class="basic_info"]/p[contains(@class,"member_title")]/text()',
            'attrib': 'text'},  
        'user_title_2' :{
            'path'  : './div/div[@class="author_info"]/div/a[contains(@class,"ipsBadge")]/text()',
            'attrib': 'text'}, 
             
             
                
        'post_date' :{
            'path'  : './div/div[@class="post_body"]/p/abbr/text()',
            'attrib': 'text',},
        'post_content'  : {
            'path'  : './div/div[@class="post_body"]/div[@itemprop="commentText"]', 
            'attrib': 'html',},
            
    }
}