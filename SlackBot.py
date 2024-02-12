import yaml
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from SlackModalLib import get_modal_view
from SlackProcessor import SlackProcessor
from DatabaseLib import init as db_lib_init

config = None
with open('config.yaml') as f:
    config = yaml.full_load(f)

app = App(token=config['BOT_TOKEN'])

@app.view("slack_db_submission")
def view_1_handle(ack, body, client):
    ack()
    
    slackProcessor = SlackProcessor(client, body)
    slackProcessor.process()

@app.block_action("select_feature")
def handle_select_feature(ack, body, client):
    ack()

@app.block_action("select_account")
def handle_select_account(ack, body, client):
    ack()
    
    modal_view = get_modal_view(body)
    view_id = body['container']['view_id']
    client.views_update(
        view_id = view_id,
        view = modal_view,
    )

@app.command('/db')
def open_modal(ack, body, client):
    if check_user_name(body['user_name']) == False:
        return ack(f"<@{body['user_id']}>\n허용되지 않은 유저입니다.")
    
    ack()
    
    modal_view = get_modal_view(body)
    client.views_open(
        trigger_id=body["trigger_id"],
        view=modal_view,
    )
    
def check_user_name(user_name):
    return user_name in config['WHITE_LIST']
    
if __name__ == '__main__':
    db_lib_init(config)
    SocketModeHandler(app, config['APP_TOKEN']).start()