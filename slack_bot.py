import os
import pandas as pd
import dataframe_image as dfi
from io import BytesIO
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import slack
import util
import time

app = App(token=bot_token)

@app.action("button-identifier")
def handle_some_action(ack, body, logger):
    ack()
    print(body)
    
@app.view("view_1")
def view_1_handle(ack, body, client):
    ack()
    
    print(body)
    db_block_id = body['view']['blocks'][0]['block_id']
    start_time_block_id = body['view']['blocks'][2]['block_id']
    end_time_block_id = body['view']['blocks'][3]['block_id']
    selected_db_list = body['view']['state']['values'][db_block_id]['multi_static_select-action']['selected_options']
    for selected_db in selected_db_list:
        print(selected_db['value'])
        
    start_time = body['view']['state']['values'][start_time_block_id]['datetimepicker-starttime']['selected_date_time']
    end_time = body['view']['state']['values'][end_time_block_id]['datetimepicker-endtime']['selected_date_time']
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    
@app.command('/grafana')
def open_modal(ack, body, client):
    # Acknowledge the command request
    ack()
    
    print(body)
    start_time = int(time.time() - (60 * 60))
    end_time = int(time.time())
    db_instance_list = util.get_options()
    channel_id = body['channel_id']
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "그라파나 캡쳐 기능"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "channel" : channel_id,
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
        }
    )
    
if __name__ == '__main__':
    SocketModeHandler(app, app_token).start()
