

http_rules = {    
    'method' : 'GET',    
    'page' : {
        'key'   : 'page',
        'value' : 1,
    },
    
    'stop' : lambda x: True,
}

elements = {
    'path': '//*[@id="container"]/div[1]',
    'attributes': {
        'user_fullname'   : {
            'path'  : './table[1]/tr/td/table/tr/td[2]/div[1]/span[2]/strong/text()', 
            'attrib': 'text'},
        'user_country'   : {
            'path'  : './table[1]/tr/td/table/tr/td[2]/div[1]/img', 
            'attrib': 'src'},
        'user_title'   : {
            'path'  : './table[1]/tr/td/table/tr/td[2]/div[1]/span[3]/text()', 
            'attrib': 'text'},
        'uid'   : {
            'path'  : './table[1]/tr/td/table/tr/td[2]/div[2]/div[1]/a', 
            'attrib': 'href', 
            'regex' : r'\d+'},
        'user_registration_birth_localTime'   : {
            'path'  : './table[1]/tr/td/table/tr/td[2]/div[2]/div[2]/span[1]/text()', 
            'attrib': 'text'},
        'user_status'   : {
            'path'  : './table[1]/tr/td/table/tr/td[2]/div[2]/div[2]/span[1]/span[1]/text()', 
            'attrib': 'text'},
            
            
        'user_additional_info'   : {
            'path'  : './div[3]/div[1]/table/tr/td[contains(@class,"scaleimages")]/text()', 
            'attrib': 'text'},
        'user_additionalgroups'   : {
            'path'  : './div[3]/div[1]/table/tr/td[contains(@id,"additionalgroups")]/ul/li/img', 
            'attrib': 'src'},
        'user_awards_color'   : {
            'path'  : './div[3]/div[1]/table/tr/td/a[contains(@href,"awards")]/../../../tr[2]/td/text()', 
            'attrib': 'text'},
        'user_awards_type'   : {
            'path'  : './div[3]/div[1]/table/tr/td/a[contains(@href,"awards")]/../../../tr[3]/td/text()', 
            'attrib': 'text'},
        'user_icq_number'   : {
            'path'  : './div[3]/div[1]/table/tr/td/span/span/img[contains(@src,"icq")]/../text()', 
            'attrib': 'text'},
        'user_yahoo_email'   : {
            'path'  : './div[3]/div[1]/table/tr/td/span/span/a[contains(@href,"yahoo.com")]/text()', 
            'attrib': 'text'},
        'user_jabber_email'   : {
            'path'  : './div[3]/div[1]/table/tr/td/a[contains(@href,"xmpp.jp")]/text()', 
            'attrib': 'text'},
            
            
            
        'user_homepage'   : {
            'path'  : './div[3]/div[2]/table/tr/td/strong[contains(text(),"Homepage")]/../../td[2]/a/text()', 
            'attrib': 'text'},
        'user_icq_number_1'   : {
            'path'  : './div[3]/div[2]/table/tr/td/a[contains(@onclick,"icq")]/text()', 
            'attrib': 'text'},
        'user_aim_screen_name'   : {
            'path'  : './div[3]/div[2]/table/tr/td/a[contains(@onclick,"aim")]/text()', 
            'attrib': 'text'},
        'user_yahoo_id'   : {
            'path'  : './div[3]/div[2]/table/tr/td/a[contains(@onclick,"yahoo")]/text()', 
            'attrib': 'text'},
            
        'user_joined'   : {
            'path'  : './div[3]/div[3]/table/tr/td/strong[contains(text(),"Joined")]/../../td[2]/text()', 
            'attrib': 'text'},
        'user_last_visit'   : {
            'path'  : './div[3]/div[3]/table/tr/td/strong[contains(text(),"Last Visit")]/../../td[2]/text()', 
            'attrib': 'text'},
        'user_total_posts'   : {
            'path'  : './div[3]/div[3]/table/tr/td/span/a[contains(@href,"finduser")]/../../text()', 
            'attrib': 'text'},
        'user_url_total_posts'   : {
            'path'  : './div[3]/div[3]/table/tr/td/span/a[contains(@href,"finduser")][2]', 
            'attrib': 'href'},
        'user_url_total_threads'   : {
            'path'  : './div[3]/div[3]/table/tr/td/span/a[contains(@href,"finduserthread")]', 
            'attrib': 'href'},
        'user_time_spend_online'   : {
            'path'  : './div[3]/div[3]/table/tr/td/strong[contains(text(),"Time Spent Online")]/../../td[2]/text()', 
            'attrib': 'text'},
        'user_reputation'   : {
            'path'  : './div[3]/div[3]/table/tr/td/strong[contains(@class,"reputation")]/text()', 
            'attrib': 'text'},
        'user_url_details_reputation'   : {
            'path'  : './div[3]/div[3]/table/tr/td/a[contains(@href,"reputation")]', 
            'attrib': 'href'},
        'user_money'   : {
            'path'  : './div[3]/div[3]/table/tr/td/a[contains(@href,"newpoints")]/text()', 
            'attrib': 'text'},
            
        
    }
    
}

new_jobs = [
#{
#    'path' : '//*[@id="container"]/div[1]/div[3]/div[3]/table/tr/td/span/a[contains(@href,"finduser")][2]',
#    'module': 'offensivecommunity.detailtotalposts',
#    'prefix': 'http://offensivecommunity.net/',
#},
#{
#    'path' : '//*[@id="container"]/div[1]/div[3]/div[3]/table/tr/td/span/a[contains(@href,"finduserthread")]',
#    'module': 'offensivecommunity.detailtotalthreads',
#    'prefix': 'http://offensivecommunity.net/',
#},
{
    'path' : '//*[@id="container"]/div[1]/div[3]/div[3]/table/tr/td/a[contains(@href,"reputation")]',
    'module': 'offensivecommunity_detailreputation',
    'prefix': 'http://offensivecommunity.net/',
}]