def init(config):
    return

def get_db_instance_list(account_name):
    db_list = list()
      
    if account_name == 'ODIN':
        db_list.append({'text' : 'odin-game001-lv - aurora-mysql', 'value' : 'odin-game001-lv'})
        db_list.append({'text' : 'odin-game002-lv - aurora-mysql', 'value' : 'odin-game002-lv'})
        db_list.append({'text' : 'odin-game003-lv - aurora-mysql', 'value' : 'odin-game003-lv'})
    elif account_name == 'ESOUL':
        db_list.append({'text' : 'esoul-game001-lv - aurora-mysql', 'value' : 'esoul-game001-lv'})
        db_list.append({'text' : 'esoul-game002-lv - aurora-mysql', 'value' : 'esoul-game002-lv'})
        db_list.append({'text' : 'esoul-game003-lv - aurora-mysql', 'value' : 'esoul-game003-lv'})
    elif account_name == 'ARCM':
        db_list.append({'text' : 'arcm-game001-lv - aurora-mysql', 'value' : 'arcm-game001-lv'})
        db_list.append({'text' : 'arcm-game002-lv - aurora-mysql', 'value' : 'arcm-game002-lv'})
        db_list.append({'text' : 'arcm-game003-lv - aurora-mysql', 'value' : 'arcm-game003-lv'})
        
    return db_list

def get_account_list():
    db_list = list()
    db_list.append({'text' : 'ODIN', 'value' : 'ODIN'})
    db_list.append({'text' : 'ESOUL', 'value' : 'ESOUL'})
    db_list.append({'text' : 'ARCM', 'value' : 'ARCM'})
    
    return db_list