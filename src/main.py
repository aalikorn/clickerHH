import keyboard as kb
import pyautogui as pgui
from pyscreeze import Box
import telegram_bot
import time
import threading

name_computer = input("Введите имя компьютера: ")
telegram_bot.name_computer = name_computer

start_text = """
Начало работы кликера (для остановки нажмите Esc)...
Если кликер работает не так как ожидается, проверьте и поменяйте скрины картинок в папке Letters.
В ней должны присутствовать Star.png, Save.png, Next.png, Cross.png, Offset.png (угол объявления, середина картинки 
находится на уровне названия объявления), Limit500.png (высвечивается при превышении лимита на 500 объявлений в день)
Также для корректной работы следует закрепить в браузере главную вкладку с поиском.
"""

telegram_bot.send_massage_print(start_text)

time.sleep(3)

lock = threading.Lock()


def process_window(window_coordinates: tuple[int, int, int, int], window_index: int):
    """
    Выполняет алгоритм для одного окна
    """

    counts = 0
    while not kb.is_pressed("Esc"):
        counts += 1
        try:
            if counts >= 10:
                telegram_bot.send_massage_print(str(window_index) + ': ' + 'Дальнейшие действия на странице не найдены')
                break
            initial_button = None

            try:
                initial_button = pgui.locateOnScreen("Letters/Star.png", confidence=0.85, region=window_coordinates)
            except pgui.ImageNotFoundException:
                print(str(window_index) + ': ' + 'Кнопка "Star" не найдена')

            if initial_button:
                lock.acquire()
                pgui.click(x=window_coordinates[0] // 2 + 20, y=window_coordinates[1] // 2 + 200)
                button = Box(initial_button.left // 2, initial_button.top // 2, initial_button.width // 2,
                             initial_button.height // 2)
                counts = 0
                pgui.click(button)
                lock.release()

                initial_save_button = None

                try:
                    initial_save_button = pgui.locateOnScreen("Letters/Save.png", confidence=0.8,
                                                              region=window_coordinates)
                except pgui.ImageNotFoundException:
                    print(str(window_index) + ': ' + 'Кнопка "Save" не найдена')

                if initial_save_button is None:
                    continue
                save_button = Box(initial_save_button.left // 2, initial_save_button.top // 2, initial_save_button.width
                                  // 2, initial_save_button.height // 2)
                clickbox = Box(save_button.left, save_button.top - 68, save_button.width, save_button.height)

                lock.acquire()
                pgui.click(x=window_coordinates[0] // 2 + 20, y=window_coordinates[1] // 2 + 200)
                pgui.click(x=clickbox.left + 10, y=clickbox.top)
                lock.release()

                try:
                    initial_save_button = pgui.locateOnScreen("Letters/Save.png", confidence=0.9, region=window_coordinates)
                    print(initial_save_button)
                    save_button = Box(initial_save_button.left // 2, initial_save_button.top // 2,
                                      initial_save_button.width
                                      // 2, initial_save_button.height // 2)
                except pgui.ImageNotFoundException:
                    print(str(window_index) + ': ' + 'Кнопка "Save" не найдена')

                lock.acquire()
                pgui.click(x=window_coordinates[0] // 2 + 20, y=window_coordinates[1] // 2 + 200)
                pgui.click(save_button)
                lock.release()

                limit = None
                try:
                    limit = pgui.locateOnScreen("Letters/Limit500.png", confidence=0.9, region=window_coordinates)
                except pgui.ImageNotFoundException:
                    pass
                if limit != None:
                    telegram_bot.send_massage_print(str(window_index) + ': ' + 'Превышен лимит 500')
                    break

                initial_offset = None
                try:
                    initial_offset = pgui.locateOnScreen("Letters/Offset.png", confidence=0.9, region=window_coordinates)
                except pgui.ImageNotFoundException:
                    print(str(window_index) + ': ' + 'Угол объявления не найден')
                if initial_offset:
                    offset = Box(initial_offset.left // 2, initial_offset.top // 2, initial_offset.width // 2,
                                 initial_offset.height // 2)
                    lock.acquire()
                    pgui.click(x=window_coordinates[0] // 2 + 20, y=window_coordinates[1] // 2 + 200)
                    pgui.click(x=offset.left + offset.width + 30, y=offset.top + offset.height / 2)
                    lock.release()

                pgui.sleep(2)

                lock.acquire()
                pgui.click(x=window_coordinates[0] // 2 + 20, y=window_coordinates[1] // 2 + 200)
                pgui.scroll(-50)


                pgui.click(x=window_coordinates[0] // 2 + 386, y=window_coordinates[1] // 2 + 68)
                lock.release()

            next_button = None
            try:
                next_button = pgui.locateOnScreen("Letters/Next.png", confidence=0.85, region=window_coordinates)
            except pgui.ImageNotFoundException:
                telegram_bot.send_massage_print(str(window_index) + ': ' + 'Кнопка "Next" не найдена')

            if next_button:
                lock.acquire()
                pgui.click(x=window_coordinates[0] // 2 + 20, y=window_coordinates[1] // 2 + 200)
                pgui.click(y=next_button.top // 2 + 5, x=next_button.left // 2 + 5)
                lock.release()
                pgui.sleep(2)
            else:
                lock.acquire()
                pgui.click(x=window_coordinates[0] // 2 + 20, y=window_coordinates[1] // 2 + 200)
                pgui.scroll(-3)
                lock.release()
        except Exception as e:
            telegram_bot.send_massage_print(f'Неизвестная ошибка\n{e}')
            break


num_windows = 4

windows_coordinates = [(0, 37 * 2, 752 * 2, 407 * 2), (754 * 2, 37 * 2, 752 * 2, 407 * 2),
                       (0 * 2, 462 * 2, 752 * 2, 407 * 2), (752 * 2, 464 * 2, 752 * 2, 407 * 2)]


threads = []

for i in range(len(windows_coordinates)):
    thread = threading.Thread(target=process_window, args=(windows_coordinates[i], i + 1))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

input("Press Enter to continue...")
