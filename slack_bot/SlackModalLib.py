import time
from DatabaseLib import get_db_instance_list, get_account_list

class ModalInfo:
    feature = None
    feature_block = None
    
    account = None
    account_block = None
    
    db_instance_list = None
    db_instance_list_block = None
    
    # default 1 hour ago
    start_time = int(time.time() - (60 * 60))
    # default now
    end_time = int(time.time())
    
    def __init__(self, body : dict):
        if body.get('view') is None:
            return
        
        if body.get('view').get('state') is None:
            return
        
        stateValues = body['view']['state']['values']
        
        self.feature = self.get_value_by_action_id(stateValues, 'select_feature')
        self.feature_block = self.get_option_by_action_id(stateValues, 'select_feature')
        
        self.account = self.get_value_by_action_id(stateValues, 'select_account')
        self.account_block = self.get_option_by_action_id(stateValues, 'select_account')
        
        self.db_instance_list_block = self.get_option_by_action_id(stateValues, 'select_db_instance')
        if self.db_instance_list_block is not None:
            self.db_instance_list = list()
            
            for row in self.db_instance_list_block:
                self.db_instance_list.append(row['value'])
        
        self.start_time = self.get_option_by_action_id(stateValues, 'start_time', self.start_time)
        self.end_time = self.get_option_by_action_id(stateValues, 'end_time', self.end_time)

    def get_option_by_action_id(self, state_values, action_id, default = None):
        for block_value in state_values.values():
            for block_action_id, action_value in block_value.items():
                if block_action_id != action_id:
                    continue
                
                for key, value in action_value.items():
                    if 'select' in key:
                        return value
        
        return default
    
    def get_value_by_action_id(self, state_values, action_id, default = None):
        for block_value in state_values.values():
            for block_action_id, action_value in block_value.items():
                if block_action_id != action_id:
                    continue
                
                for key, value in action_value.items():
                    if 'select' in key and value is not None:
                        return value['value']
        
        return default

def get_value_by_action_id(self, state_values, action_id, default = None):
    for block_value in state_values.values():
        for block_action_id, action_value in block_value.items():
            if block_action_id != action_id:
                continue
            
            for key, value in action_value.items():
                if 'select' in key and value is not None:
                    return value['value']
    
    return default

def get_option_by_action_id(self, state_values, action_id, default = None):
    for block_value in state_values.values():
        for block_action_id, action_value in block_value.items():
            if block_action_id != action_id:
                continue
            
            for key, value in action_value.items():
                if 'select' in key:
                    return value
    
    return default

def get_modal_view(body : dict):
    modal_view = {}
    modalInfo = ModalInfo(body)
    # 어카운트의 DB 목록
    account_db_list = get_db_instance_list(modalInfo.account)
    # 그전에 선택한 DB 목록
    select_db_list = modalInfo.db_instance_list_block
    # 위의 두 목록을 결합
    combine_db_list = combine_options_initial_options(account_db_list, select_db_list)

    modal_view['type'] = 'modal'
    modal_view['callback_id'] = 'slack_db_submission'
    modal_view['title'] = get_plain_text('DB운영 슬랙 기능')
    modal_view['submit'] = get_plain_text('실행')
    modal_view['private_metadata'] = body.get('private_metadata', body.get('channel_id', '')) 
    modal_view['blocks'] = list()
    modal_view['blocks'].append(get_static_select('기능 선택', 'select_feature', get_feature_list(), modalInfo.feature_block))
    modal_view['blocks'].append(get_divider())
    modal_view['blocks'].append(get_static_select('어카운트 선택', 'select_account', get_account_list(), modalInfo.account_block))
    modal_view['blocks'].append(get_divider())
    
    # 선택 가능한 DB목록이 있을 경우
    if len(combine_db_list) > 0:
        modal_view['blocks'].append(get_multi_static_select('DB 인스턴스 선택', 'select_db_instance', combine_db_list, select_db_list))
        
    modal_view['blocks'].append(get_divider())
    modal_view['blocks'].append(get_datetimepicker('StartTime', 'start_time', modalInfo.start_time))
    modal_view['blocks'].append(get_datetimepicker('EndTime', 'end_time', modalInfo.end_time))
    
    return modal_view

def get_modal_view_v2(body : dict):
    modal_view = {}
    modal_view['type'] = 'modal'
    modal_view['callback_id'] = 'slack_db_submission'
    modal_view['title'] = get_plain_text('DB운영 슬랙 기능')
    modal_view['submit'] = get_plain_text('실행')
    modal_view['blocks'] = list()
    modal_view['blocks'].append(get_divider())
    modal_view['blocks'].append(get_file_input('쿼리 입력', 'input_query'))
    
    return modal_view
    
def get_plain_text(text):
    return {"type" : "plain_text", "text" : text}

def get_divider():
    return {"type" : "divider"}

def get_static_select(text, action_id, options, initial_option = None):
    block = {"type" : "input", "dispatch_action" : True, "element" : {"type" : "static_select", "placeholder" : {"type" : "plain_text", "text" : "Select an item"},
                    "options" : convert_to_options(options), "action_id" : action_id}, "label" : {"type" : "plain_text", "text" : text}}
                  
    # 선택한 옵션이 있을 경우
    if initial_option is not None:
        block['element']['initial_option'] = initial_option
    
    return block

def get_multi_static_select(text , action_id, options, initial_options = None):
    block = {"type" : "input", "element" : {"type" : "multi_static_select", "placeholder" : {"type" : "plain_text", "text" : "Select an item"},
                    "options" : convert_to_options(options), "action_id" : action_id}, "label" : {"type" : "plain_text", "text" : text}}
    
    # 선택한 옵션이 있을 경우
    if initial_options is not None:
        if len(initial_options) > 0:
            block['element']['initial_options'] = initial_options
    
    return block
    
def get_plain_text_input(text, action_id):
    return {"type" : "input", "element" : {"type" : "plain_text_input", "action_id" : action_id, "multiline": True}, "label" : {"type" : "plain_text", "text" : text}}

def get_file_input(text, action_id):
    return {"type" : "input", "element" : {"type" : "file_input", "action_id" : action_id, "filetypes" : ["sql", "txt"]}, "label" : {"type" : "plain_text", "text" : text}}  
    
def get_datetimepicker(text, action_id, initial_date_time):
    return {"type" : "input", "element" : {"type" : "datetimepicker", "initial_date_time" : initial_date_time, "action_id" : action_id}, "label" : {"type" : "plain_text", "text" : text, "emoji" : True}}

def convert_to_options(element_list : dict): 
    options = list()
    
    for option in element_list:
        options.append({"text" : {"type" : "plain_text", "text" : option['text'], "emoji" : True}, "value" : option['value']})
    
    return options

# 선택 가능한 옵션은 최대 100개
def combine_options_initial_options(options : list, initial_options : list):# 선택된 옵션이 없을 경우 옵션 목록만 반환
    if initial_options is None:
        return options[:100]
    
    # 선택된 옵션이 있을 경우 우선 선택된 옵션을 더해준다.
    combine_options = list()
    for initial_option in initial_options:
        combine_options.append({'text' : initial_option['text']['text'], 'value' : initial_option['value']})
    
    for option in options:
        exists = False
        for initial_option in initial_options:
            value = initial_option['value']
            
            if value == option['value']:
                exists = True
                break
            
        if exists == False:    
            combine_options.append(option)
        
    return combine_options[:100]

def get_feature_list():
    feature_list = list()
    feature_list.append({'text' : '그라파나 캡쳐', 'value' : 'grafana'})
    feature_list.append({'text' : '슬로우 쿼리', 'value' : 'slowquery'})
    feature_list.append({'text' : '프로세스 리스트', 'value' : 'processlist'})
    
    return feature_list

if __name__ == '__main__':
    bb = ModalInfo({})
    