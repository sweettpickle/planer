import telebot
from telebot import types

# bot = telebot.TeleBot('%ваш токен%')
token = '1010919676:AAFlETQiiF6PUzGctcTFtNZLzCb12aVJjt4'
bot = telebot.TeleBot(token)

# обработчик сообщений
@bot.message_handler(commands=['start'])
def welcome(message):
    # bot.reply_to(message, message.text)
    # bot.send_message(message.chat.id, "Привет!")
    # users[message.chat.id] = track
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttom1 = types.KeyboardButton("Список привычек")
    buttom2 = types.KeyboardButton("Добавить привычку")
    buttom3 = types.KeyboardButton("Удалить привычку")
    menu.add(buttom1, buttom2, buttom3)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=menu)

done = "\u274c"
not_done = "\u2b55\ufe0f"
key = ''

def create_progress(n):
    lst = []
    for i in range(n):
        lst.append(not_done)
    return lst

track = {
    "Спорт": create_progress(21),
    "Чтение 30 минут": create_progress(21)
}

users = {}

@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text == "Список привычек":
        inline = types.InlineKeyboardMarkup(row_width=1)
        # for key in track.keys():
        for key in users[message.chat.id].keys():
            inline.add(types.InlineKeyboardButton(key, callback_data=key))
        bot.send_message(message.chat.id, "Ваш список привычек:", reply_markup=inline)

    if message.text == "Добавить привычку":
        bot.register_next_step_handler(message, add_tracker)
        bot.send_message(message.chat.id, "Введите название:")

    if message.text == "Удалить привычку":
        bot.register_next_step_handler(message, del_tracker)
        bot.send_message(message.chat.id, "Введите название:")

def add_tracker(message):
    # if message.text in track:
    if message.text in users[message.chat.id]:
        bot.send_message(message.chat.id, "Привычка с таким названием уже есть")
    else:
        global key
        key = message.text
        bot.register_next_step_handler(message, add_tracker2)
        bot.send_message(message.chat.id, "Введите количество дней:")

def add_tracker2(message):
    # track[key] = create_progress(int(message.text))
    users[message.chat.id][key] = create_progress(int(message.text))
    bot.send_message(message.chat.id, "Привычка добавлена")


def del_tracker(message):
    # if message.text in track:
    if message.text in users[message.chat.id]:
        track.pop(message.text)
        bot.send_message(message.chat.id, "Привычка удалена")
    else:
        bot.send_message(message.chat.id, "Такой привычки нет")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # if call.data in track:
    if call.data in users[call.message.chat.id]:
        global key
        key = call.data
        inline = types.InlineKeyboardMarkup(row_width=1)
        # but = types.InlineKeyboardButton(''.join(track[key]), callback_data="check")
        but = types.InlineKeyboardButton(''.join(users[call.message.chat.id][key]), callback_data="check")
        inline.add(but)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=key, reply_markup=inline)
    elif call.data == "check":
        # check(key)
        check(key, call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=key, reply_markup=None)
        inline = types.InlineKeyboardMarkup(row_width=1)
        but = types.InlineKeyboardButton(''.join(track[key]), callback_data="check")
        inline.add(but)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=key, reply_markup=inline)
        bot.answer_callback_query(call.id, text="Отмечено")


# def check(key):
def check(key, id):
    # lst = track.get(key)
    lst = users[id].get(key)
    for i in range(len(lst)):
        if lst[i] == not_done:
            lst[i] = done
            break
    track[key] = lst

bot.polling(none_stop=True)
