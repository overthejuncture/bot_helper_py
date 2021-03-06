from telegram.callbackquery import CallbackQuery
import json
from . import utils

def is_pager_action(callback: CallbackQuery):
    if not isinstance(callback, str):
        data = json.loads(callback.data)
    else: 
        data = json.loads(callback)
    return True if data.get('start') != None else False

def get_action(callback: CallbackQuery):
    data = json.loads(callback.data)
    action = data.get(utils.ACTION_LITERAL)
    return action, data.get(utils.DATA_LITERAL)

def get_data(callback: CallbackQuery):
    data = json.loads(callback.data)
    return data.get(utils.DATA_LITERAL)