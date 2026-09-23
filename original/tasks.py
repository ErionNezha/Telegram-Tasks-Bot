import telebot
from telebot import types


bot = telebot.TeleBot("Token Bot")

user_tasks = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    btn1 = types.InlineKeyboardButton('إضافة مهمة', callback_data="add")
    btn2 = types.InlineKeyboardButton('حذف مهمة', callback_data="'delete")
    btn3 = types.InlineKeyboardButton('المهام', callback_data="tasks")
    azrar = types.InlineKeyboardMarkup(row_width=1)
    azrar.add(btn1, btn2, btn3)
    
    bot.send_message(chat_id, 'اختار الزر الي يعحبك .', reply_markup=azrar)
@bot.callback_query_handler(func=lambda call: call.data == "add")
def add(call):
    chat_id = call.message.chat.id
    bot.edit_message_text("٫ دز هسه المهمة الي تريد تضيفة ٬", chat_id, call.message.message_id)
    bot.register_next_step_handler(call.message, save)
    
def save(message):
    task = message.text
    user_id = message.chat.id    
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    user_tasks[user_id].append(task)

    bot.send_message(user_id, "* - تم اضافة المهمة *")


@bot.callback_query_handler(func=lambda call: call.data == "'delete")
def delete(call):
    chat_id = call.message.chat.id
    
    if chat_id not in user_tasks or len(user_tasks[chat_id]) == 0:
        bot.send_message(chat_id, "ماكو مهمام اصلا علمود تحذفة !")
    else:
        btn4 = types.InlineKeyboardButton('الغاء', callback_data='cancel')        
        azrar = types.InlineKeyboardMarkup(row_width=1)
        for i, task in enumerate(user_tasks[chat_id]):
            Deleted = types.InlineKeyboardButton(task, callback_data=str(i))
            azrar.add(Deleted)
            azrar.add(btn4)
        
        bot.send_message(chat_id, "*اختار المهمة الي تريد تحذفة *", reply_markup=azrar)


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def remove(call):
    task_index = int(call.data)
    chat_id = call.message.chat.id
    
    if chat_id not in user_tasks or task_index < 0 or task_index >= len(user_tasks[chat_id]):
        bot.send_message(chat_id, "رقم مو صالح .")
    else:
        dele = user_tasks[chat_id].pop(task_index)
        bot.edit_message_text("تم مسح هذا المهمة ← " + dele , chat_id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def cancel(call):
    chat_id = call.message.chat.id
    
    bot.edit_message_text("تم الغاء مسح المهام ", chat_id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "tasks")
def tasks(call):
    chat_id = call.message.chat.id
    
    if chat_id not in user_tasks or len(user_tasks[chat_id]) == 0:
        bot.edit_message_text("ماعندك مهام .", chat_id, call.message.message_id)
    else:
        task = '\n- '.join(user_tasks[chat_id])
        bot.edit_message_text("مهامك :\n- " + task, chat_id, call.message.message_id)


bot.infinity_polling()