from typing import (
    List,
    Callable,
    Union,
    Tuple
)
import logging
import json

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from django.db.models import (
    Model,
    QuerySet
)


def check(update: Update):
    print(update.message.from_user.id)

def listAll(list: List[Model], field: Callable = lambda x:x.name) -> str:
    return "\n".join("{idx}. {text}".format(idx=idx+1, text=field(x)) for idx, x in enumerate(list))

def list_with_keyboard(
    list: List[Model],
    start: int = 0,
    limit: int = 10,
    field: Callable = lambda x:x.name,
    n_cols: int = 2
):
    list = list.all()[start:start+limit+1]

    show_next = False if len(list) != limit+1 else True
    show_prev = False if start == 0 else True

    list = list[0:10]
    text = listAll(list, field)
    buttons = []
    for idx, item in enumerate(list):
        buttons.append(InlineKeyboardButton(text=idx + 1, callback_data=item.pk))
    footer_buttons = make_footer_buttons(start, limit, show_prev=show_prev, show_next=show_next)
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols, footer_buttons=footer_buttons))
    return text, reply_markup

def make_footer_buttons(
    start: int = 0,
    limit: int = 10,
    show_prev: bool = True,
    show_next: bool = True
) -> List[InlineKeyboardButton]:
    buttons = []
    if show_prev:
        buttons.append(InlineKeyboardButton(
                '<',
                callback_data=json.dumps({"start": start - limit, "limit": limit})
            )
        )
    if show_next:
        buttons.append(InlineKeyboardButton(
                '>',
                callback_data=json.dumps({"start": start + limit, "limit": limit})
            )
        )
    return buttons


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

def proccess_pager(update: Update) -> Tuple[int, int]:
    # TODO make pager class or smth
    data = json.loads(update.callback_query.data)
    start = data.get('start')
    limit = data.get('limit')
    return int(start), int(limit)