import pymysql
import json
import time

def execute(text):
    data = dict()
    
    try:    
        db = pymysql.connect(host="localhost", port=4401, user="root", password="1234", db="", charset='utf8')
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(text)
        data = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        db.close()
        
    return data

def get_options():
    li_db_list = list()
    li_db_list.append('esoul-game01-lv')
    li_db_list.append('esoul-game02-lv')
    li_db_list.append('odin-game001-lv')
    li_db_list.append('odin-game002-lv')
   
    option_list = list()
    for db in li_db_list:
        db_dict = {'text' : {'type' : 'plain_text', 'text' : db, 'emoji' : True}, 'value' : db}
        option_list.append(db_dict)

    return option_list

if __name__ == '__main__':
    #print(get_options())
    print(time.time() - 60 * 60)