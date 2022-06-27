from typing import (
    List,
    Callable,
    Union
)

import json

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from django.db.models import Model

def check(update: Update):
    print(update.message.from_user.id)

def listAll(list: List[Model], field: Callable = lambda x:x.name) -> str:
    return "\n".join("{idx}. {text}".format(idx=idx+1, text=field(x)) for idx, x in enumerate(list))

def list_with_keyboard(
    list: List[Model],
    field: Callable = lambda x:x.name,
    n_cols: int = 2
):
    text = listAll(list, field)
    buttons = []
    for idx, item in enumerate(list):
        buttons.append(InlineKeyboardButton(text=idx + 1, callback_data=item.pk))
    footer_buttons = make_footer_buttons()
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols))
    return text, reply_markup

def make_footer_buttons(start: int = 0, limit: int = 10, show_prev: bool = True, show_next: bool = True):
    prev = InlineKeyboardButton('<', callback_data=json.dumps({"start": start, "limit": limit}))
    buttons = [
    ]
    pass

def make_previous_button(start: int = 0, limit: int = 10):
    start = start - limit if start - limit > 0 else 0
    button = InlineKeyboardButton('<', callback_data=json.dumps({'start': start, 'limit': limit}))

def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu