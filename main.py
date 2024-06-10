from tkinter import *
import random
from tkinter import ttk, messagebox
import re

from PIL import Image, ImageTk

import sqlite3 as sl

con = sl.connect('thecode.db')
con.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY,
              login TEXT NOT NULL,
              password TEXT NOT NULL)
              ''')
con.execute('''CREATE TABLE IF NOT EXISTS data_users
             (id INTEGER PRIMARY KEY,
              name1 TEXT,
              name2 TEXT,
              name3 TEXT,
              age INTEGER,
              user_id INTEGER NOT NULL)
              ''')

cursor = con.cursor()


def validate_login(log_name):
    pattern = r"^[a-zA-Z0-9_-]{3,16}$"
    if re.match(pattern, log_name):
        return True
    else:
        messagebox.showerror("Ошибка",
                             "Логин должен содержать от 3 до 16 символов и может содержать только буквы, цифры, "
                             "символы подчеркивания и дефисы.")
        return False


def validate_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.match(pattern, password):
        return True
    else:
        messagebox.showerror("Ошибка", "Длина пароля должна быть не менее 8 символов.\n"
                                       "Пароль должен содержать хотя бы одну строчную букву.\n"
                                       "Пароль должен содержать хотя бы одну заглавную букву.\n"
                                       "Пароль должен содержать хотя бы одну цифру.\n"
                                       "Пароль должен содержать хотя бы один из следующих специальных символов: @, $, "
                                       "!, %, *, ?, &.")
        return False


def find_user_by_login(log_name):
    sql_select_query = """select * from users where login = ?"""
    cursor.execute(sql_select_query, (log_name,))
    records = cursor.fetchall()
    return records


def find_profile_by_user_id(id_user):
    sql_select_query = """select * from data_users where user_id = ?"""
    cursor.execute(sql_select_query, (id_user,))
    records = cursor.fetchall()
    return records


def registration():
    global InpPassReg1
    global InpPassReg2
    global InpLogReg
    if InpLogReg.get() != "" and InpPassReg1.get() != "" and InpPassReg2.get() != "":
        if validate_login(InpLogReg.get()) and validate_password(InpPassReg1.get()):
            user = find_user_by_login(InpLogReg.get())
            if not user and InpPassReg1.get() == InpPassReg2.get():

                cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)',
                               (InpLogReg.get(), InpPassReg1.get()))
                con.commit()
                user = find_user_by_login(InpLogReg.get())
                cursor.execute('INSERT INTO data_users (name1, name2, name3, age, user_id) VALUES (?, ?, ?, ?, ?)',
                               ("", "", "", 0, int(user[0][0])))
                con.commit()
                root.destroy()
                profile(user[0][0])
            elif InpPassReg1.get() != InpPassReg2.get():
                messagebox.showerror("Error", "Пароли не совпадают")
            else:
                messagebox.showerror("Error", "такой логин уже существует")
        else:
            return
    else:
        messagebox.showerror("Error", "Заполните все поля")


def validate_last_name(last_name):
    if not last_name.isalpha():
        messagebox.showerror("Ошибка", "Фамилия должна содержать только буквы и не должна быть пустой")
        return False
    return True


def validate_first_name(first_name):
    if not first_name.isalpha():
        messagebox.showerror("Ошибка", "Имя должно содержать только буквы и не должно быть пустым")
        return False
    return True


def validate_middle_name(middle_name):
    if not middle_name.isalpha():
        messagebox.showerror("Ошибка", "Отчество должно содержать только буквы и не должно быть пустым")
        return False
    return True


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def get_element_from_grid(grid, row, column):
    for child in grid.winfo_children():
        if int(child.grid_info()["row"]) == row and int(child.grid_info()["column"]) == column:
            return child
    return False


def validate_answer(frame, num):
    if num == 0:
        messagebox.showerror("Ошибка", "Решите все примеры")
        return False
    for i in range(num):
        if get_element_from_grid(frame, i + 2, 1).get() == "":
            messagebox.showerror("Ошибка", "Решите все примеры")
            return False
    return True


def check_window(window):
    if not window.winfo_exists():
        return False

    window.destroy()
    return True


def validate_params(drop1, drop2, scale):
    if drop1 != "" and drop2 != "" and scale != "":
        return True
    else:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return False


def profile(user_id):
    winProf = Tk()
    winProf.geometry('{}x{}'.format(x, y))
    winProf.resizable(False, False)
    winProf.title('Profile')

    def close_and_create_window(winProf):
        winProf.destroy()

        def generate_example(choice, period_start, period_end, num_examples, frame):
            def check_answer(frame, examples_arr):
                if not validate_answer(frame, len(examples_arr)):
                    return

                count_t = 0
                count_f = 0
                for i in range(len(examples_arr)):
                    examples_arr[i].append(int(get_element_from_grid(frame, i + 2, 1).get()))
                    if examples_arr[i][1] == examples_arr[i][2]:
                        Label(frame, text="Правильно", font=("JetBrains Mono", 18, "bold")).grid(row=i + 2, column=2,
                                                                                                 padx=20,
                                                                                                 pady=10)
                        count_t += 1
                    else:
                        Label(frame, text=f"Неправильно, ответ будет {examples_arr[i][1]}",
                              font=("JetBrains Mono", 18, "bold")).grid(row=i + 2,
                                                                        column=2, padx=20, pady=10)
                        count_f += 1
                get_element_from_grid(frame, row=len(examples_arr) + 2, column=0).destroy()
                Label(frame, font=("JetBrains Mono", 16), text=f"Верно: {count_t}\nНеверно: {count_f}", ).grid(
                    row=len(examples_arr) + 2, column=0)
                parent_window = frame.winfo_toplevel()
                Button(frame, text="Назад", background="#ADC5C3", font=("JetBrains Mono", 20), padx=10, pady=10,
                       command=lambda: close_and_create_window(parent_window)).grid(
                    row=len(examples_arr) + 2, column=1)

            examples_arr = []
            for i in range(num_examples):
                a = random.randint(period_start, period_end)
                b = random.randint(period_start, period_end)
                if choice == "Сложение":
                    examples_arr.append([f"{a} + {b} = ", a + b])
                elif choice == "Вычитание":
                    examples_arr.append([f"{a} - {b} = ", a - b])
                elif choice == "Умножение":
                    examples_arr.append([f"{a} x {b} = ", a * b])
                else:
                    examples_arr.append([f"{a} : {b} = ", a // b])
            for i in range(len(examples_arr)):
                label = Label(frame, text=f"{examples_arr[i][0]}", font=("JetBrains Mono", 18, "bold"))
                label.grid(row=i + 2, column=0, padx=20, pady=10)
                inp_answer = Entry(frame)
                inp_answer.grid(row=i + 2, column=1, padx=20, pady=10)
            btn_check = Button(frame, background="#ADC5C3", font=("JetBrains Mono", 20), text="Проверить", padx=30, pady=10,
                               command=lambda: check_answer(frame, examples_arr))
            btn_check.grid(row=len(examples_arr) + 2, column=0, columnspan=2)

        def run_math(dropdown_type, hard, num_examples):
            if validate_params(dropdown_type, hard, num_examples):
                hard_choice = None
                hard_num = [[1, 20], [20, 80], [80, 150]]
                if hard == "лёгкий":
                    hard_choice = hard_num[0]
                elif hard == "нормальный":
                    hard_choice = hard_num[1]
                elif hard == "сложный":
                    hard_choice = hard_num[2]
                clear_frame(params)
                generate_example(dropdown_type, hard_choice[0], hard_choice[1], num_examples, params)
            else:
                return

        params_window = Tk()
        params_window.geometry('{}x{}'.format(x, y))
        params_window.resizable(False, False)
        params_window.title('Параметры')
        params = Frame(params_window, width=x * 0.5, height=y * 0.5, )
        params.place(anchor="center", relx=0.5, rely=0.3)
        Label(params, font=("JetBrains Mono", 32, "bold"), pady=10, text="Настрой примеры под себя").grid(row=0,
                                                                                                          column=0)
        Label(params, font=("JetBrains Mono", 20), pady=10, text="Выбери тип примера").grid(row=1, column=0)
        options = ["Сложение", "Вычитание", "Умножение", "Целочисленное деление"]
        dropdown = ttk.Combobox(params, values=options)
        dropdown.config(width=30)
        dropdown.config(font=('Arial', 18))
        dropdown.grid(row=2, column=0)
        label_difficulty = Label(params, font=("JetBrains Mono", 20), pady=10, text="Выберите уровень сложности:")
        label_difficulty.grid(row=3, column=0)
        difficulty_options = ["лёгкий", "нормальный", "сложный"]
        difficulty_dropdown = ttk.Combobox(params, values=difficulty_options)
        difficulty_dropdown.config(width=30)
        difficulty_dropdown.config(font=('Arial', 18))
        difficulty_dropdown.grid(row=4, column=0)
        label_examples = Label(params, font=("JetBrains Mono", 20), pady=10, text="Выбери количество примеров:")
        label_examples.grid(row=5, column=0)
        scale = Scale(params, from_=1, to=20, orient=HORIZONTAL, length=300)
        scale.grid(row=6, column=0)
        label_easy = Label(params, font=("JetBrains Mono", 20), pady=10, text="Лёгкий - числа от 1 до 20")
        label_easy.grid(row=1, column=1)
        label_normal = Label(params, font=("JetBrains Mono", 20), pady=10, text="Нормальный - числа от 20 до 80")
        label_normal.grid(row=2, column=1)
        label_hard = Label(params, font=("JetBrains Mono", 20), pady=10, text="Сложный - числа от 80 до 150")
        label_hard.grid(row=3, column=1)
        btn_save = Button(params, background="#ADC5C3", font=("JetBrains Mono", 20), text="Начать", padx=30, pady=10,
                          command=lambda: run_math(dropdown.get(), difficulty_dropdown.get(), scale.get()))
        btn_save.grid(row=7, column=0)

        def Undo():
            params_window.destroy()
            profile(user_id)

        btn_undo = Button(params, font=("JetBrains Mono", 20), background="#ADC5C3", text="Назад", padx=30, pady=10,
                          command=lambda: Undo())
        btn_undo.grid(row=7, column=1, columnspan=2)

        params_window.mainloop()

    def Update_profile(name1, name2, name3, age):
        if validate_last_name(name1) and validate_first_name(name2) and validate_middle_name(name3):
            cursor.execute('UPDATE data_users SET name1 =?, name2 =?, name3 =?, age =? WHERE user_id =?',
                           (name1, name2, name3, age, user_id))
            con.commit()
            entry_users()
            user_data(user_id)
        else:
            return

    def change_frame(frame1, frame2, posx, posy):
        frame1.place(anchor="center", relx=0.5, rely=0.5)
        show_frame(frame1)
        hide_frame(frame2)

    def show_frame(frame):
        frame.tkraise()

    def hide_frame(frame):
        frame.place_forget()

    container = Frame(winProf, height=y * 0.5, width=x * 0.5, background="#DDD9CF")
    container.grid(row=2, column=1, sticky="nsew", columnspan=3)

    Label(winProf, text="Пользователь", font=("JetBrains Mono", 18, "bold")).grid(row=1, column=0, sticky="nsew")

    avatar_frame = Frame(winProf)
    avatar = Image.open("./images/avatar.png")
    avatar = avatar.resize((int(x * 0.2), int(x * 0.2)))
    avatar_img = ImageTk.PhotoImage(avatar)
    ttk.Label(avatar_frame, image=avatar_img, background="#D9D9D9").pack()
    avatar_frame.grid(row=2, column=0, sticky="nsew")

    button_page_one = Button(winProf, text="Информация", background="#ADC5C3", font=("Arial", 18),
                             highlightbackground="yellow", highlightthickness=2, padx=10, pady=10,
                             command=lambda: change_frame(start_frame, page_one_frame, 100, 100))
    button_page_one.grid(row=1, column=1, )
    button_page_two = Button(winProf, text="Настройки", background="#ADC5C3", font=("Arial", 18),
                             highlightbackground="yellow", highlightthickness=2, padx=10, pady=10,
                             command=lambda: change_frame(page_one_frame, start_frame, 200, 25))
    button_page_two.grid(row=1, column=2)
    button_page_three = Button(winProf, text="Приступить", background="#ADC5C3", font=("Arial", 18),
                               highlightbackground="yellow", highlightthickness=2, padx=10, pady=10,
                               command=lambda: close_and_create_window(winProf))
    button_page_three.grid(row=1, column=3)

    start_frame = Frame(container, background="#D9D9D9")
    page_one_frame = Frame(container, background="#D9D9D9")

    change_frame(start_frame, page_one_frame, 100, 100)

    def user_data(u_id):
        clear_frame(start_frame)
        Label(start_frame, text=f'Профиль', font=("JetBrains Mono", 32, "bold")).grid(row=0, column=0, columnspan=2)
        inf_user = find_profile_by_user_id(u_id)[0]
        labels_name = ["Фамилия", "Имя", "Отчество", "Возраст"]
        for i in range(len(labels_name)):
            Label(start_frame, text=f'{labels_name[i]}', background="#D9D9D9",
                  font=("JetBrains Mono", 18, "bold")).grid(row=i + 1, column=0)
            if inf_user[i + 1] == 0 or inf_user[i + 1] == "":
                Label(start_frame, text=f"Не указано", background="#D9D9D9", font=("JetBrains Mono", 18)).grid(
                    row=i + 1, column=1)
            else:
                Label(start_frame, text=f"{inf_user[i + 1]}", background="#D9D9D9", font=("JetBrains Mono", 18)).grid(
                    row=i + 1, column=1)

    user_data(user_id)

    def entry_users():
        clear_frame(page_one_frame)
        inf_user = find_profile_by_user_id(user_id)[0]
        label_page_one = Label(page_one_frame, text="Настройки", font=("JetBrains Mono", 32, "bold"))
        label_page_one.pack(pady=10, padx=10)
        label_surname = Label(page_one_frame, background="#D9D9D9", text="Фамилия:", font=("JetBrains Mono", 16))
        label_surname.pack()
        entry_surname = Entry(page_one_frame, background="#ADC5C3", font=("JetBrains Mono", 16), borderwidth=5,
                              relief="ridge")
        entry_surname.insert(0, inf_user[1])
        entry_surname.pack()
        label_name = Label(page_one_frame, background="#D9D9D9", text="Имя:", font=("JetBrains Mono", 16))
        label_name.pack()
        entry_name = Entry(page_one_frame, background="#ADC5C3", font=("JetBrains Mono", 16), borderwidth=5,
                           relief="ridge")
        entry_name.insert(0, inf_user[2])
        entry_name.pack()
        label_patronymic = Label(page_one_frame, background="#D9D9D9", text="Отчество:", font=("JetBrains Mono", 16))
        label_patronymic.pack()
        entry_patronymic = Entry(page_one_frame, background="#ADC5C3", font=("JetBrains Mono", 16), borderwidth=5,
                                 relief="ridge")
        entry_patronymic.insert(0, inf_user[3])
        entry_patronymic.pack()
        label_age = Label(page_one_frame, background="#D9D9D9", text="Возраст:", font=("JetBrains Mono", 16))
        label_age.pack()
        entry_age = Scale(page_one_frame, from_=1, to=100, orient=HORIZONTAL)
        entry_age.pack()
        entry_age.set(inf_user[4])
        button_start = Button(page_one_frame,font=("JetBrains Mono", 20), background="#ADC5C3", text="Сохранить", padx=30, pady=10,
                              command=lambda: Update_profile(entry_surname.get(), entry_name.get(),
                                                             entry_patronymic.get(), entry_age.get()))
        button_start.pack()

    entry_users()
    show_frame(start_frame)
    winProf.mainloop()


def login():
    global InpLog
    global InpPass
    if InpLog.get() != "" and InpPass.get() != "":
        user = find_user_by_login(InpLog.get())
        if user and user[0][1] == InpLog.get() and user[0][2] == InpPass.get():
            root.destroy()
            profile(user[0][0])

        else:
            messagebox.showerror("Error", "Неверный логин или пароль")
    else:
        messagebox.showerror("Error", "Пожалуйста, заполните все поля")


root = Tk()
x = int(root.winfo_screenwidth() * 0.8)  # размер  по горизонтали
y = int(root.winfo_screenheight() * 0.8)  # размер по вертикали

root.geometry('{}x{}'.format(x, y))
root.resizable(False, False)
root.title('Math train')

#  вкладки
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

frame1 = Frame(notebook, width=x, height=y - int(x * 0.1), background="#D9D9D9")
frame2 = Frame(notebook, width=x, height=y, background="#D9D9D9")

frame1.pack()
frame2.pack(fill='both', expand=True)

reg_logo = Image.open("./images/reg.png")
reg_logo = reg_logo.resize((int(x * 0.19), int(y * 0.1)))
reg_logo_img = ImageTk.PhotoImage(reg_logo)

log_logo = Image.open("./images/log.png")
log_logo = log_logo.resize((int(x * 0.1), int(y * 0.1)))
log_logo_img = ImageTk.PhotoImage(log_logo)

image1 = Image.open("./images/elem1.png")
image1 = image1.resize((int(image1.size[0]), int(image1.size[1])))
test = ImageTk.PhotoImage(image1)
ttk.Label(frame1, image=test, background="#D9D9D9").place(x=0, y=0)
ttk.Label(frame2, image=test, background="#D9D9D9").place(x=0, y=0)

image2 = Image.open("./images/elem2.png")
test2 = ImageTk.PhotoImage(image2)
ttk.Label(frame1, image=test2, background="#D9D9D9").place(x=x - test2.width(), y=0)
ttk.Label(frame2, image=test2, background="#D9D9D9").place(x=x - test2.width(), y=0)

image3 = Image.open("./images/elem3.png")
test3 = ImageTk.PhotoImage(image3)
ttk.Label(frame1, image=test3, background="#D9D9D9").place(x=x - test3.width(), y=y - test3.height() - (y * 0.15))
ttk.Label(frame2, image=test3, background="#D9D9D9").place(x=x - test3.width(), y=y - test3.height() - (y * 0.15))

image4 = Image.open("./images/elem4.png")
test4 = ImageTk.PhotoImage(image4)
ttk.Label(frame1, image=test4, background="#D9D9D9").place(x=0, y=y - test4.height() - (y * 0.15))
ttk.Label(frame2, image=test4, background="#D9D9D9").place(x=0, y=y - test4.height() - (y * 0.15))

notebook.add(frame1, image=reg_logo_img)
notebook.add(frame2, image=log_logo_img)

Label(frame2, text="Вход", foreground="black", font=("JetBrains Mono", 32, "bold")).place(x=image1.width + 10,
                                                                                          y=image1.height / 2)
InpLog = Entry(frame2, font=("JetBrains Mono", 20), background="#ADC5C3", borderwidth=10, relief="ridge")
InpLog.place(x=image1.width + 10, y=image1.height, width=x * 0.275, height=y * 0.08)
Label(frame1, text="⬅ Придумай логин").place(x=image1.width + 10 + x * 0.275 + 10, y=image1.height + y * 0.08 / 3.5)
Label(frame2, text="⬅ Введи логин").place(x=image1.width + 10 + x * 0.275 + 10, y=image1.height + y * 0.08 / 3.5)

InpPass = Entry(frame2, font=("JetBrains Mono", 20), background="#ADC5C3", borderwidth=10, relief="ridge", show="*")
InpPass.place(x=image1.width + 10, y=image1.height + y * 0.08 + y * 0.05, width=x * 0.275, height=y * 0.08)
Label(frame1, text="⬅ Придумай пароль").place(x=image1.width + 10 + x * 0.275 + 10,
                                              y=image1.height + y * 0.08 + y * 0.05 + y * 0.08 / 3.5)
Label(frame2, text="⬅ Введи пароль").place(x=image1.width + 10 + x * 0.275 + 10,
                                           y=image1.height + y * 0.08 + y * 0.05 + y * 0.06 / 3.5)

SendBtn = Button(frame2, text="Войти", padx=10, pady=10, command=login)
SendBtn.place(x=image1.width + 10, y=image1.height + y * 0.08 + y * 0.175, width=x * 0.275, height=y * 0.08)

Label(frame1, text="Регистрация", foreground="black", font=("JetBrains Mono", 32, "bold")).place(x=image1.width + 10,
                                                                                                 y=image1.height / 2)

InpLogReg = Entry(frame1, font=("JetBrains Mono", 20), background="#ADC5C3", borderwidth=10, relief="ridge")
InpLogReg.place(x=image1.width + 10, y=image1.height, width=x * 0.275, height=y * 0.08)

InpPassReg1 = Entry(frame1, font=("JetBrains Mono", 20), background="#ADC5C3", borderwidth=10, relief="ridge", show="*")
InpPassReg1.place(x=image1.width + 10, y=image1.height + y * 0.08 + y * 0.05, width=x * 0.275, height=y * 0.08)

InpPassReg2 = Entry(frame1, font=("JetBrains Mono", 20), background="#ADC5C3", borderwidth=10, relief="ridge", show="*")
InpPassReg2.place(x=image1.width + 10, y=image1.height + y * 0.08 + y * 0.05 + y * 0.125, width=x * 0.275,
                  height=y * 0.08)
Label(frame1, text="⬅ Подтверди пароль").place(x=image1.width + 10 + x * 0.275 + 10,
                                               y=image1.height + y * 0.08 + y * 0.05 + y * 0.08 + y * 0.07)
SendBtnReg = Button(frame1, text="Зарегистрироваться", command=registration)
SendBtnReg.place(x=image1.width + 10, y=image1.height + y * 0.08 + y * 0.3, width=x * 0.275, height=y * 0.08)
root.mainloop()

con.commit()
con.close()
