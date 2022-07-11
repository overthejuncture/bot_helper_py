from typing import (
    List,
    Callable,
    Union,
    Tuple,
    Dict
)
import json

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import (
    CallbackContext
)

from django.db.models import Model
from django.db.models.query import QuerySet

ACTION_LITERAL = 'a'
DATA_LITERAL = 'd'
EDIT_ACTION = 'e'
DELETE_ACTION = 'd'
LIMIT_DEFAULT = 10

MODEL_TITLE_DEFAULT = lambda x: x.title

def list_all(list: List[Model], field: Callable = lambda x:x.name) -> str:
    return "\n".join("{idx}. {text}".format(idx=idx+1, text=field(x)) for idx, x in enumerate(list))

def list_with_keyboard_and_pager(
    list: List[Model],
    start: int = 0,
    limit: int = None,
    field: Callable = None,
    n_cols: int = 2,
):
    return _list_with_keyboard(list, start, limit, field, n_cols, make_pager=True)

def _list_with_keyboard(
    list: List[Model],
    start: int = 0,
    limit: int = None,
    field: Callable = None,
    n_cols: int = 2,
    make_pager: bool = False
):
    limit = limit or LIMIT_DEFAULT
    field = field or MODEL_TITLE_DEFAULT

    list = list.all()[start:start+limit+1]

    show_next = False if len(list) != limit+1 else True
    show_prev = False if start == 0 else True

    list = list[0:limit]
    text = list_all(list, field)
    buttons = []
    for idx, item in enumerate(list):
        buttons.append(InlineKeyboardButton(text=idx + 1, callback_data=json.dumps({DATA_LITERAL: {'id': item.pk}})))
    footer_buttons = make_pager_buttons(start, limit, show_prev=show_prev, show_next=show_next) if make_pager else []
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols, footer_buttons=footer_buttons))
    return text, reply_markup

def make_pager_buttons(
    start: int = 0,
    limit: int = None,
    show_prev: bool = True,
    show_next: bool = True
) -> List[InlineKeyboardButton]:
    limit = limit or LIMIT_DEFAULT
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

def create_action_buttons(data: Dict = {}, edit: bool = False, delete: bool = False) -> List[List[InlineKeyboardButton]]:
    buttons = []
    if edit:
        buttons.append(InlineKeyboardButton('Изменить', callback_data=json.dumps({ACTION_LITERAL: EDIT_ACTION, DATA_LITERAL: data})))
    if delete:
        buttons.append(InlineKeyboardButton('Удалить', callback_data=json.dumps({ACTION_LITERAL: DELETE_ACTION, DATA_LITERAL: data})))
    return [buttons]

def pager(func):
    def wrapper(update: Update, context: CallbackContext):
        start, limit = proccess_pager(update)
        params = func(update, context)
        if isinstance(params, QuerySet):
            list = params
            field = MODEL_TITLE_DEFAULT
        else:
            list, field = params

        text, r_m = list_with_keyboard_and_pager(list, start, limit, field=field)
        update.callback_query.edit_message_text(text, reply_markup=r_m)

    return wrapper