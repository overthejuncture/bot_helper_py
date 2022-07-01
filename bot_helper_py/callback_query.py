from ast import Call
from telegram.callbackquery import CallbackQuery
import json
from . import bot

def is_pager_action(callback: CallbackQuery):
    data = json.loads(callback.data)
    return True if data.get('start') != None else False

def get_action(callback: CallbackQuery):
    data = json.loads(callback.data)
    action = data.get(bot.ACTION_LITERAL)
    return action, data.get(bot.DATA_LITERAL)

def get_data(callback: CallbackQuery):
    data = json.loads(callback.data)
    return data.get(bot.DATA_LITERAL)