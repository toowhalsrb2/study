import datetime
from SlackModalLib import ModalInfo

class SlackProcessor:
    def __init__(self, client, body) -> None:
        modalInfo = ModalInfo(body)
        
        self.client = client
        self.user_id = body['user']['id']
        self.channel = body['view']['private_metadata']
        self.feature = modalInfo.feature
        self.account = modalInfo.account
        self.db_instance_list = modalInfo.db_instance_list
        self.start_time = modalInfo.start_time
        self.end_time = modalInfo.end_time
        
        response = self.send_message(f"기능 : {self.feature}\nDB 인스턴스 목록 : {', '.join(self.db_instance_list)}\n{datetime.datetime.fromtimestamp(self.start_time)} ~ {datetime.datetime.fromtimestamp(self.end_time)}")
        self.thread_ts = response['ts']
        
    def send_message(self, text):
        response = self.client.chat_postMessage(channel=self.user_id, text=text)
        return response
    
    def send_message_to_reply(self, text):
        response = self.client.chat_postMessage(channel=self.user_id, text=text, thread_ts=self.thread_ts)
        return response
        
    def send_file(self, filename, title, content):
        try:
            response = self.client.files_upload_v2(filename=filename, title=title, content=content)
            permalink = response['files'][0]['permalink']
            self.send_message(permalink)
        except Exception as e:
            #self.send_message(str(e))
            print(str(e))
            
    def send_file_to_reply(self, filename, title, content):
        try:
            response = self.client.files_upload_v2(filename=filename, content=content, thread_ts=self.thread_ts)
            permalink = response['files'][0]['permalink']
            self.send_message_to_reply(permalink)
        except Exception as e:
            #self.send_message(str(e))
            print(str(e))
        
    def process(self):
        if self.feature == 'grafana':
            self.grafana_process()
        elif self.feature == 'slowquery':
            self.slowquery_process()
        elif self.feature == 'processlist':
            self.processlist_process()
        else:
            self.send_message(f'Invalid Feature : {self.feature}')
        return
    
    def grafana_process(self):
        return
        
    def slowquery_process(self):
        return
    
    def processlist_process(self):
        return