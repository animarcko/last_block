from tkinter import *
import re
import pickle
import hashlib
from random import randint
from tkinter import messagebox


def clear_window():
    """Удаление всех объектов из окна."""
    for widget in root.winfo_children():
        widget.destroy()


def hash_password(password):
    """Хэширование пароля для безопасного хранения."""
    return hashlib.sha256(password.encode()).hexdigest()


def write(record, filename):
    """Сохранение данных в файл."""
    with open(filename, "wb") as file:
        pickle.dump(record, file)


def read(filename):
    """Чтение данных из файла."""
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return {}


def sign_in():
    """Вход и регистрация"""
    clear_window()

    # Загрузка фона регистрации
    sign_in_img = PhotoImage(file="sign_in (2).png")
    sign_in = Label(root, image=sign_in_img)
    sign_in.image = sign_in_img
    sign_in.pack()

    Label(root, text="LOGIN (EMAIL)", font=("Roboto", 9), bg="#FFDE97").place(
        relx=0.395, rely=0.54, anchor="c"
    )
    Label(root, text="PASSWORD", font=("Roboto", 9), bg="#FFDE97").place(
        relx=0.381, rely=0.64, anchor="c"
    )

    global e1, e2
    e1 = Entry(root, width=33, bg="#FFDE97")
    e2 = Entry(root, show="*", width=33, bg="#FFDE97")
    e1.place(relx=0.497, rely=0.59, anchor="c")
    e2.place(relx=0.497, rely=0.69, anchor="c")

    global error_label
    error_label = Label(root, text="", fg="black", bg="#F49751", font=("Roboto", 10))
    error_label.place(relx=0.5, rely=0.738, anchor="c")

    sign_btn = Button(
        root,
        text="Sign In",
        command=lambda: check_login(e1.get(), e2.get(), gender.get()),
        font=("Roboto", 11),
        height=1,
        width=14,
        bg="#FFDE97",
    )
    sign_btn.place(relx=0.5, rely=0.80, anchor="c")

    reg_btn = Button(
        root,
        text="Registration",
        command=lambda: save_credentials(e1.get(), e2.get(),gender),
        font=("Roboto", 11),
        height=1,
        width=14,
        bg="#FFDE97",
    )
    reg_btn.place(relx=0.5, rely=0.88, anchor="c")
    #выбор гендера
    Label(root, text="GENDER",font=("Roboto", 10),bg="#FFDE97")\
                .place(relx = 0.369, rely = 0.48, anchor = "c")

    gender = StringVar(value="not selected")
    man_radio = Radiobutton (
        root,
        text = "man",
        font=("Roboto", 9),
        bg="#FFDE97",
        variable = gender,
        value = "man"
        )
    man_radio.place(relx = 0.50, rely = 0.48, anchor = "c")
    
    woman_radio = Radiobutton(
        root,
        text = "woman",
        font=("Roboto", 9),
        bg="#FFDE97",
        variable = gender,
        value = "woman"
        )
    woman_radio.place(relx = 0.62, rely = 0.48, anchor = "c")


def contains_special_characters(s):
    """Проверка на наличие специальных символов."""
    return bool(re.search(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/~`]', s))


def is_valid_email(email):
    """Проверка корректности формата электронной почты с помощью регулярного выражения."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


def check_login(login, password,gender):
    """Проверка логина и пароля."""
    error_label.config(text="")
    #проверка полей на заполненность
    if not login or not password or gender == "not selected":
        error_label.config(text="Поля не заполнены!")
        return

    # Проверка на корректность формата электронной почты
    if not is_valid_email(login):
        error_label.config(text="Введите корректный адрес электронной почты!")
        return

    credentials = read("credentials.pkl")
    # Проверка на существование пользователя
    if credentials:
        if login in credentials and credentials[login]["password"] == hash_password(
            password
        ):
            global current_player
            current_player = login
            messagebox.showinfo("WELCOME", f"HELLO, {current_player}! WELCOME TO MAIN MENU OF LAST BRICK!")
            main_menu()
        else:
            error_label.config(text="Неверный логин или пароль!")
    else:
        error_label.config(text="В игре еще нет учетных записей!")


def save_credentials(login, password,gender):
    """Сохранение учетных данных в файл."""

    # Проверка на заполненность полей
    if not login or not password or gender == "not selected":
        error_label.config(text="Поля не заполнены!")
        return

    # Проверка на корректность формата электронной почты
    if not is_valid_email(login):
        error_label.config(text="Введите корректный адрес электронной почты!")
        return

    # Проверка на наличие специальных символов
    if not contains_special_characters(password):
        error_label.config(text="Пароль должен содержать специальные символы!")
        return

    # Проверка на длину пароля
    if len(password) < 8:
        error_label.config(text="Пароль должен быть больше 8 символов!")
        return

    # Чтение существующих учетных данных
    credentials = read("credentials.pkl")

    # Проверка на существование учетной записи
    if credentials and login in credentials:
        error_label.config(text="Учетная запись уже существует!")
        return

    # Добавляем для хранения учетных данных
    credentials[login] = {"password": hash_password(password)}

    # Сохранение новых учетных данных в файл
    write(credentials, "credentials.pkl")

    # Добавляем для хранения статистики
    stats = read("stats.pkl")
    stats[login] = {"wins": 0, "losses": 0}

    # Сохранение новых записи в файл
    write(stats, "stats.pkl")
    error_label.config(text="Учетные данные сохранены!")


def show_rules():
    """Правила игры."""
    clear_window()
    # Загрузка фона правил
    rules_img = PhotoImage(file="rules.png")
    rules_pic = Label(root, image=rules_img)
    rules_pic.image = rules_img
    rules_pic.pack()

    rules_label = Label(
        root,
        text="""The total number of bricks sets randomly.\n
Alternately, the bot and the player take from 1 to 3 bricks.\n
The one who takes the last one wins.""",
        font=("Roboto", 13),
        justify=LEFT,
        bg="#FFE2BF",
        fg="#852633",
    )

    rules_label.place(relx=0.5, rely=0.73, anchor="c")
    # Кнопка возврата в меню
    back_btn = Button(
        root,
        text="Back",
        command=main_menu,
        font=("Roboto", 13),
        bg="#FFEBD2",
        fg="#852633",
    )
    back_btn.place(relx=0.83, rely=0.815, anchor="c")


def turn(amount):
    global bricks_amount, comp_do, winner_txt, win_stat_int, lose_stat_int
    bricks_amount -= amount
    if bricks_amount <= 0:  # Выигрыш
        win_stat_int += 1
        update_result(1, 0)  # Добавляем победу в статистику
        winner_txt["text"] = "WIN"
        winner_txt["fg"] = "green"
        winner_txt["bg"] = "#cef0c9"
        win_stat_txt["text"] = f"WINS: {win_stat_int}\nLOSES: {lose_stat_int}"
        disable()  # Отключение элементов управления
    elif bricks_amount < 4:  # Автоматический проигрыш
        lose_stat_int += 1  # Заносится в статистику
        update_result(0, 1)  # Добавляем проигрыш в статистику
        comp_do["text"] = "BOT TOOK {0}".format(bricks_amount)
        bricks_amount = 0  # Обнуление
        winner_txt["text"] = "LOSE :("
        winner_txt["fg"] = "red"
        winner_txt["bg"] = "#ffc0cb"
        win_stat_txt["text"] = (
            f"WINS: {win_stat_int}\nLOSES: {lose_stat_int}"  # Статистика
        )
        disable()
    else:  # Ход компьютера
        comp_turn = randint(1, min(3, bricks_amount))
        bricks_amount -= comp_turn
        comp_do["text"] = "BOT TOOK {0}".format(comp_turn)
        comp_do["font"] = ("Arial", 14)

    # Обновление состояния кнопок
    update_button_state()
    bricks_txt["text"] = str(bricks_amount)  # Остаток кирпичей


def update_button_state():
    if bricks_amount == 1:
        take_two["state"] = DISABLED
        take_three["state"] = DISABLED
    elif bricks_amount == 2:
        take_three["state"] = DISABLED
    elif bricks_amount <= 0:
        take_one["state"] = DISABLED
        take_two["state"] = DISABLED
        take_three["state"] = DISABLED
    else:
        take_one["state"] = NORMAL
        take_two["state"] = NORMAL
        take_three["state"] = NORMAL


# Создание функции перезапуска
def play_again():
    global comp_do, bricks_amount, bricks_txt, winner_txt, win_stat_int, lose_stat_int
    comp_do["text"] = "YOUR TURN"  # Изменяет надпись хода компьютера
    comp_do["font"] = ("Arial", 12)
    bricks_amount = randint(12, 20)
    bricks_txt["text"] = str(bricks_amount)  # Изменяет счетчик кирпичей
    winner_txt["fg"] = "#FFC060"  # Делаем надпись победы невидимой
    winner_txt["bg"] = "#FFC060"
    enable()  # Включение кнопок


# Функция включения всех кнопок
def enable():
    take_one["state"] = NORMAL
    take_two["state"] = NORMAL
    take_three["state"] = NORMAL


# Функция отключения всех кнопок
def disable():
    take_one["state"] = DISABLED
    take_two["state"] = DISABLED
    take_three["state"] = DISABLED


# Функция сохранения статистики в файл
def update_result(wins, loses):
    stats = read("stats.pkl")
    stats[current_player]["wins"] += wins
    stats[current_player]["losses"] += loses
    write(stats, "stats.pkl")


def main_game():
    global root, win_stat_int, lose_stat_int, bricks_amount, bricks_txt, comp_do, winner_txt, win_stat_txt, take_one, take_two, take_three

    # Инициализация глобальных переменных
    win_stat_int = 0
    lose_stat_int = 0
    bricks_amount = randint(12, 20)

    clear_window()
    # Загрузка фона
    game_img = PhotoImage(file="game.png")
    game_pic = Label(root, image=game_img)
    game_pic.image = game_img
    game_pic.pack()

    # Создание кнопок для ходов
    take_one = Button(
        text="1 BRICK",
        width=15,
        font=("Arial", 9),
        bg="#FFFDC0",
        fg="#e52b50",
        command=lambda amount=1: turn(amount),
    )
    take_one.place(relx=0.25, rely=0.88, anchor="c")

    take_two = Button(
        text="2 BRICKS",
        width=15,
        font=("Arial", 9),
        bg="#FFFDC0",
        fg="#e52b50",
        command=lambda amount=2: turn(amount),
    )
    take_two.place(relx=0.5, rely=0.88, anchor="c")

    take_three = Button(
        text="3 BRICKS",
        width=15,
        font=("Arial", 9),
        bg="#FFFDC0",
        fg="#e52b50",
        command=lambda amount=3: turn(amount),
    )
    take_three.place(relx=0.75, rely=0.88, anchor="c")

    # Создание счетчика кирпичей
    brick_label = Label(
        root, text="NUMBER OF BRICKS:", font=("Arial", 23), bg="#FFFDC0"
    )
    brick_label.place(relx=0.5, rely=0.1, anchor="c")

    bricks_txt = Label(root, text=str(bricks_amount), font=("Arial", 23), bg="#FFFDC0")
    bricks_txt.place(relx=0.5, rely=0.2, anchor="c")

    comp_do = Label(text="YOUR TURN", font=("Arial", 14), bg="#FFFDC0", fg="#e52b50")
    comp_do.place(relx=0.5, rely=0.3, anchor="c")

    # Создание объяснений игроку и имен соперников

    player_hint_txt = Label(
        text="TAKE :", font=("Arial", 12), bg="#6C1835", fg="#FFFDC0"
    )
    player_hint_txt.place(relx=0.5, rely=0.78, anchor="c")

    winner_txt = Label(root, font=("Arial", 20), fg="#cfcfcf", bg="#FFC060")
    winner_txt.place(relx=0.48, rely=0.6, anchor="c")

    win_stat_txt = Label(
        root,
        text=f"WINS: {win_stat_int}\nLOSES: {lose_stat_int}",
        font=("Arial", 10),
        bg="#480442",
        fg="#FFFDC0",
    )
    win_stat_txt.place(relx=0.1, rely=0.5, anchor="c")

    # Кнопка для перезапуска игры
    restart_button = Button(
        root, text="REPLAY", bg="#9C3D36", fg="#FFFDC0", command=play_again
    )
    restart_button.place(relx=0.87, rely=0.37, anchor="c")

    # Кнопка меню
    menu_button = Button(
        root, text="MENU", bg="#9C3D36", fg="#FFFDC0", command=main_menu
    )
    menu_button.place(relx=0.865, rely=0.3, anchor="c")


def display_statistics():
    clear_window()
    # Загрузка фона
    try:
        stat_img = PhotoImage(file="score.png")
        stat_pic = Label(root, image=stat_img)
        stat_pic.image = stat_img
        stat_pic.pack()

    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return  # Завершение функции в случае ошибки

    # Кнопка возврата в меню
    back_btn = Button(
        root,
        text="Back",
        command=main_menu,
        font=("Roboto", 9),
        bg="#FFC060",
        height=1,
        width=17,
    )
    back_btn.place(relx=0.5, rely=0.88, anchor="c")
    # Загрузка статистики
    stats = read("stats.pkl")

    frame = Frame(root)
    frame.pack()
    frame.place(relx=0.5, rely=0.2, anchor="n")
    
    total_stats = []
    for user, stat in stats.items():
        if stat["wins"] == 0 and stat["losses"] == 0:
            rate = 0
        else:
            rate = (
                round(stat["wins"] / (stat["losses"] + stat["wins"]) * 100, 2)
                if stat["losses"] != 0
                else 100
            )
        total_stats.append((user, stat["wins"], stat["losses"], rate))

    total_stats.sort(key=lambda x: x[3], reverse=True)
    total_stats = total_stats[:10]  # Ограничение на 10 записей
    headers = ["Player", "Wins", "Losses", "Win Rate"]
    total_stats.insert(0, headers)

    total_rows = len(total_stats)
    total_columns = len(total_stats[0])

    for i in range(total_rows):
        for j in range(total_columns):
            e = Entry(
                frame,
                width=16,
                font=("Roboto", 7),
                fg="black",
                disabledforeground="black",
                disabledbackground="#FFC060",
            )
            e.insert(END, str(total_stats[i][j]))
            e.configure(state="disabled")
            e.grid(row=i, column=j)
            
def exit_game():
    """Закрытие приложения."""
    messagebox.askyesno("EXIT", f"DO YOU REALLY WANT TO EXIT?")
    root.destroy()

def main_menu():
    """Отображение главного меню."""
    clear_window()
    # Загрузка фона меню
    menu_img = PhotoImage(file="menu_back.png")
    menu_pic = Label(root, image=menu_img)
    menu_pic.image = menu_img
    menu_pic.pack()

    current_player_label = Label(
        root, text=f"Player: {current_player}", font=("Roboto", 9), bg="#FFDE97"
    )
    current_player_label.place(relx=0.75, rely=0.05, anchor="c")

    # Кнопки меню
    btn_rules = Button(
        root, text="RULES", bg="#FFDE97", height=2, width=30, command=show_rules
    )
    btn_rules.place(relx=0.5, rely=0.58, anchor="c")

    btn_play = Button(
        root, text="PLAY", bg="#FFDE97", height=2, width=30, command=main_game
    )
    btn_play.place(relx=0.5, rely=0.68, anchor="c")

    btn_score = Button(
        root,
        text="SCORE",
        bg="#FFDE97",
        height=2,
        width=30,
        command=lambda: display_statistics(),
    )
    btn_score.place(relx=0.5, rely=0.78, anchor="c")

    back_btn = Button(
        root,
        text="SIGN OUT",
        bg="#FFDE97",
        height=2,
        width=30,
        command=sign_in,
    )
    back_btn.place(relx=0.5, rely=0.88, anchor="c")

    exit_btn = Button(root, text="X", bg="#FFDE97", height=1, width=2, command=exit_game)
    exit_btn.place(relx=0.95, rely=0.05, anchor="c")



def start():
    """Отображение главного меню."""
    clear_window()

    # Загрузка фона меню
    start_img = PhotoImage(file="start.png")
    start_pic = Label(root, image=start_img)
    start_pic.image = start_img
    start_pic.pack()

    # Кнопка начать
    btn_start = Button(
        root,
        text="START",
        font=("Roboto", 15),
        bg="#FFDE97",
        height=2,
        width=33,
        command=sign_in,
    )
    btn_start.place(relx=0.5, rely=0.54, anchor="c")


# Создание окна игры
root = Tk()
root.title("LAST BLOCK")
root.geometry("543x440")
root.resizable(False, False)
start()
root.mainloop()
