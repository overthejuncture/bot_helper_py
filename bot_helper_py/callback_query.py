from telegram.callbackquery import CallbackQuery
import json

def is_pager_action(callback: CallbackQuery):
    data = json.loads(callback.data)
    return True if data.get('start') != None else False
