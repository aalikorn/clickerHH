from notifiers import get_notifier
from sys import exit as sysexit


token = ''
chat_id_list = []
with open('id_list.env','r') as file:
    chat_id_list = file.readlines()
chat_id_list = [id_str.split('#')[0].strip() for id_str in chat_id_list if id_str.split('#')[0].strip()]

token = chat_id_list[0].split('=')
if len(token) != 2:
    print('Неверно указан токен!')
    input("Press Enter to continue...")
    sysexit(1)
token = token[1].strip()
del chat_id_list[0]

name_computer = ''
telegram = get_notifier('telegram')

def send_massage_print(message, is_print = True):
    try:
        for id in chat_id_list:
            telegram.notify(raise_on_errors=True, token=token, chat_id=id, message=name_computer + ' : ' + message)
    except Exception as e:
        print(e)
        print(f"ошибка отправки уведомления: {e}")
        input("Press Enter to continue...")
        sysexit(1)
    if is_print:
        print(name_computer + ' : ' + message)

