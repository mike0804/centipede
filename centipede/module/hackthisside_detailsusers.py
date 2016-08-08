

http_rules = {    
    'method' : 'GET',
    
    'stop' : lambda x: True,
}

elements = {
    'path': '//*[@id="viewprofile"]',
    'attributes': {
        'user_groups'   : {
            'path'  : './div/div/dl/dd/select/option[contains(@selected,"selected")]/../option/text()', 
            'attrib': 'text'},
        'user_url_blog'   : {
            'path'  : './div/div/dl/dd/a[contains(@href,"blog")]', 
            'attrib': 'href'},
        'user_blog'   : {
            'path'  : './div/div/dl/dd/a[contains(@href,"blog")]/text()', 
            'attrib': 'text'},
        'user_contact_info'   : {
            'path'  : './div/div/div/h3[contains(text(),"Contact")]/../dl[contains(@class,"details")]', 
            'attrib': 'html'},
        'user_status'   : {
            'path'  : './div/div/div/h3[contains(text(),"statistics")]/../dl[contains(@class,"details")]', 
            'attrib': 'html'},
        
    }
    
}