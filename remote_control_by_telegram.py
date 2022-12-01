import telebot
from telebot import types
import pyautogui
import win32gui
import win32process
import os
import time

bot = telebot.TeleBot('token')

# Программи которие скрипт будет отслеживать
MY_TUSKS = ['task1', 'task2', 'task3', '...']

# Название и путь к программе
MY_TUSKS_PATH = {'task1': "E:\\your\\path\\to\\file",
                 'task2': "E:\\your\\path\\to\\file",
                 'task3': "E:\\your\\path\\to\\file",
                 '...': "E:\\your\\path\\to\\file",
                 }
dict_tasks = {}


def winEnumHandler( hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)

        dict_tasks[win32gui.GetWindowText(hwnd)] = current_pid


def close_task(pid):
    os.system("taskkill /pid " + str(pid))


def open_task(task_name):
    os.startfile(MY_TUSKS_PATH[task_name])


@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    pyautogui.screenshot('screenshot.png')
    bot.send_photo(576030168, open("screenshot.png", 'rb'))


@bot.message_handler(commands=['reload_list'])
def reload_list(message):
    dict_tasks.clear()
    win32gui.EnumWindows(winEnumHandler, None)

    for my_task in MY_TUSKS:
        is_reply = False
        for task in dict_tasks.keys():
            if my_task in task:
                markup_inline = types.InlineKeyboardMarkup(row_width=2)
                key_1 = types.InlineKeyboardButton("Закрыть", callback_data=f'close {dict_tasks[task]}')
                key_2 = types.InlineKeyboardButton("Перезагрузить", callback_data=f'reload {my_task} {dict_tasks[task]}')
                markup_inline.add(key_1, key_2)
                bot.send_message(message.chat.id, my_task, reply_markup=markup_inline, disable_notification=True)
                is_reply = True
                break

        if not is_reply:
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            markup_inline.add(types.InlineKeyboardButton("Открыть", callback_data=f'open {my_task}'))
            bot.send_message(message.chat.id, my_task, reply_markup=markup_inline, disable_notification=True)


@bot.callback_query_handler(func=lambda call: True)
def anwser(call):
    data = call.data.split()
    print(data)

    if data[0] == 'close':
        close_task(data[1])
    elif data[0] == 'open':
        open_task(data[1])
    elif data[0] == 'reload':
        close_task(data[2])
        time.sleep(90)
        open_task(data[1])


if __name__ == '__main__':
    bot.infinity_polling()

