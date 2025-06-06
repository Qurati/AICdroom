from AI.multi_ans import *
from db import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.kb_title import *


def start_kb(msg):
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    user_id = msg.from_user.id
    conn, cursor = get_cursor()
    cursor.execute("SELECT AI FROM profile WHERE user_id = %s", (user_id,))
    ai = cursor.fetchone()[0]
    main_kb.add()

    if ai =="GPT":
        main_kb.add(KeyboardButton(profile), KeyboardButton(change_model))
        main_kb.add(KeyboardButton(change_AI), KeyboardButton(change_role))
        main_kb.add(KeyboardButton(context_title), KeyboardButton(settings)) # save_chats -> context_title
    else:
        main_kb.add(KeyboardButton(profile), KeyboardButton(change_AI))
        main_kb.add(KeyboardButton(change_role), KeyboardButton(context_title)) # save_chats -> context_title
        main_kb.add(KeyboardButton(settings))
    return main_kb

def get_subscription_kb(channel: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(subscribe, url=f"https://t.me/{channel.lstrip('@')}")],
        [InlineKeyboardButton(subscribed, callback_data="check_subscription")]
    ])




def slots_kb(user_id):
    slot1 = InlineKeyboardButton(get_slot_name(user_id, 1), callback_data='slot_1')
    slot2 = InlineKeyboardButton(get_slot_name(user_id, 2), callback_data='slot_2')
    slot3 = InlineKeyboardButton(get_slot_name(user_id, 3), callback_data='slot_3')
    btn_list = [slot1, slot2, slot3]
    slots_num_kb = InlineKeyboardMarkup(row_width=1).add(*btn_list)
    return slots_num_kb
return_btn = InlineKeyboardButton(back, callback_data='return_btn')

rename_btn1 = InlineKeyboardButton(rename, callback_data='rename_slot_1')
save_btn1 = InlineKeyboardButton(save, callback_data='save_1')
load_btn1 = InlineKeyboardButton(download, callback_data='load_1')
delete_btn1 = InlineKeyboardButton(delete, callback_data='delete_1')
btn_list = [rename_btn1, save_btn1, load_btn1, delete_btn1, return_btn]
slot1 = InlineKeyboardMarkup(row_width=1).add(*btn_list)

rename_btn2 = InlineKeyboardButton(rename, callback_data='rename_slot_2')
save_btn2 = InlineKeyboardButton(save, callback_data='save_2')
load_btn2 = InlineKeyboardButton(download, callback_data='load_2')
delete_btn2 = InlineKeyboardButton(delete, callback_data='delete_2')
btn_list = [rename_btn2, save_btn2, load_btn2, delete_btn2, return_btn]
slot2 = InlineKeyboardMarkup(row_width=1).add(*btn_list)

rename_btn3 = InlineKeyboardButton(rename, callback_data='rename_slot_3')
save_btn3 = InlineKeyboardButton(save, callback_data='save_3')
load_btn3 = InlineKeyboardButton(download, callback_data='load_3')
delete_btn3 = InlineKeyboardButton(delete, callback_data='delete_3')
btn_list = [rename_btn3, save_btn3, load_btn3, delete_btn3, return_btn]
slot3 = InlineKeyboardMarkup(row_width=1).add(*btn_list)


change_AI_kb = ReplyKeyboardMarkup(resize_keyboard=True)
change_AI_kb.add(KeyboardButton(chat_gpt))
change_AI_kb.add(KeyboardButton(yandex_gpt))
change_AI_kb.add(KeyboardButton(giga_chat))
change_AI_kb.add(KeyboardButton(back))


change_model_kb = ReplyKeyboardMarkup(resize_keyboard=True)
change_model_kb.add(KeyboardButton(gpt_model1))
change_model_kb.add(KeyboardButton(gpt_model2))
change_model_kb.add(KeyboardButton(gpt_model3))
change_model_kb.add(KeyboardButton(gpt_model4))
change_model_kb.add(KeyboardButton(back))


def multi_mode_kb(user_id, multi_mode_change=multi_mode_change, multi_mode=multi_mode):
    settings_inline_kb = InlineKeyboardMarkup(row_width=1)
    multi_mode = InlineKeyboardButton(
        f"{multi_mode} {'✅' if is_multi_mode(user_id) else '❌'}",
        callback_data="toggle_multi_mode"
    )
    btn_list = [multi_mode]
    settings_inline_kb.add(*btn_list)
    print(is_multi_mode(user_id))
    if is_multi_mode(user_id):
        multi_mode_change = InlineKeyboardButton(multi_mode_change, callback_data="edit_ai_set")
        settings_inline_kb.add(multi_mode_change)

    return settings_inline_kb


role_kb = ReplyKeyboardMarkup(resize_keyboard=True)
role_kb.add(
    KeyboardButton(teacher),
    KeyboardButton(psycho)
)
role_kb.add(KeyboardButton(tech),
    KeyboardButton(prog))
role_kb.add(KeyboardButton(assist))
role_kb.add(KeyboardButton(back))

credit_btns = InlineKeyboardMarkup(row_width=1)

credit_btns.add(InlineKeyboardButton(
        buy_credits,
        callback_data="buy_credits"
))
credit_btns.add(InlineKeyboardButton(
        buy_quest,
        callback_data="buy_requests"
))

context_kb = ReplyKeyboardMarkup(resize_keyboard=True)
context_kb.add(
    KeyboardButton(save_chats),
    KeyboardButton(delete_context),     #ДОПОЛНИТЬ
)
context_kb.add(
    KeyboardButton(back)
)

delete_context_btns = InlineKeyboardMarkup(row_width=2)

delete_context_btns.add(InlineKeyboardButton(
        delete_context_true,
        callback_data="deleting_context_true"),
        InlineKeyboardButton(
                delete_context_false,
                callback_data="deleting_context_false"
        )
)