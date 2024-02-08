class SlackCommandModal:
    def __init__(self):
        self.type = 'modal'
        self.callback_id = 'db_func'
        self.title = self.get_plain_text('DB운영 슬랙 기능')
        self.submit = self.get_plain_text('실행')
        self.blocks = list()
        self.blocks.append(self.get_multi_static_select(['a','b','c'], 'cc', 'bb'))

    def get_plain_text(self, text):
        return {"type" : "plain_text", "text" : text}

    def get_multi_static_select(self, option_list : list, action_id : str, label_text : str):
        return {"type" : "input", "accessory" : {"type" : "multi_static_select", "placeholder" : {"type" : "plain_text", "text" : "Select options", "emoji" : True}, "options" : self.list_convert_to_options(option_list), "action_id" : action_id},
        "label" : {"type" : "plain_text", "text" : label_text, "emoji" : True}}

    def list_convert_to_options(self, option_list : list):
        converted_option_list = list()
        for option in option_list:
            converted_option_list.append({"text" : {"type" : "plain_text", "text" : option, "emoji" : True}, "value" : option})
        
        return converted_option_list

"""
"type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "그라파나 캡쳐 기능"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                    {
                        "type": "input",
                        "element": {
                            "type": "multi_static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select options",
                                "emoji": True
                            },
                            "options": db_instance_list,
                            "action_id": "multi_static_select-action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "DB Instance",
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "datetimepicker",
                            "initial_date_time" : start_time,
                            "action_id": "datetimepicker-starttime"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Start Time",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "datetimepicker",
                            "initial_date_time" : end_time,
                            "action_id": "datetimepicker-endtime"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "End Time",
                            "emoji": True
                        }
                    }
                ]
"""

if __name__ == '__main__':
    aa = SlackCommandModal()
    print(aa.__dict__)
