import os
import pandas as pd
import dataframe_image as dfi
from io import BytesIO
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import slack
import bot_util
import time
import GrafanaLib
import json

APP_TOKEN = 'xapp-1-A06GN6EGEM8-6578870418337-8a5b50cc93897860777b56291b22797cc63e4598978ee6eeda27964375ddd340'
BOT_TOKEN = 'xoxb-16162981047-6578873569153-ZNlnOrR1saszKUfZJAObIdP7'

app = App(token=BOT_TOKEN)

@app.action("button-identifier")
def handle_some_action(ack, body, logger):
    ack()
    print(body)
    
@app.view("grafana_view_select_account")
def view_1_handle(ack, body, client):
    ack()
    print('view')
    print(body)

@app.action("test_action")
def handle_block_action(ack, body, client):
    ack()
    print(body)

    start_time = int(time.time() - (60 * 60))
    end_time = int(time.time())
    db_instance_list = bot_util.get_options()

    view_id = body['container']['view_id']

    client.views_update(
        # Pass a valid trigger_id within 3 seconds of receiving it
        view_id = view_id,
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "DB운영팀"},
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
        }
    )

@app.command('/test')
def open_modal(ack, body, client):
    ack()
    print(body)
    start_time = int(time.time() - (60 * 60))
    end_time = int(time.time())
    account_list = bot_util.get_account_list()

    channel_id = body['channel_id']
    command = body['command']
    text = body['text']
    #response = client.chat_postMessage(channel=channel_id, text=f'{command} {text}')

    thread_ts = 0
    # Call views_open with the built-in client
    print(f'channel : {channel_id}, ts : {thread_ts}')
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "grafana_view_select_account",
            "private_metadata": json.dumps(body),
            "title": {"type": "plain_text", "text": "그라파나 캡쳐 기능"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "This is a section block with a button."
                            },
                            "accessory": {
                                "type": "multi_static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select options",
                                "emoji": True
                            },
                            "options": bot_util.get_account_list(),
                            "action_id": "test_action"
                            },
                        }
                    ]
        }
    )
    
if __name__ == '__main__':
    SocketModeHandler(app, APP_TOKEN).start()
