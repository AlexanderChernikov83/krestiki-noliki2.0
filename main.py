import tkinter as tk
from tkinter import messagebox

# --- глобальные переменные ---
current_player = "X"
buttons = []
score = {"X": 0, "O": 0}
target_wins = 3   # игра до трёх побед
game_active = True


# --- функции ---
def check_winner():
    # строки и столбцы
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            highlight([buttons[i][0], buttons[i][1], buttons[i][2]])
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            highlight([buttons[0][i], buttons[1][i], buttons[2][i]])
            return True

    # диагонали
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        highlight([buttons[0][0], buttons[1][1], buttons[2][2]])
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        highlight([buttons[0][2], buttons[1][1], buttons[2][0]])
        return True

    return False


def check_draw():
    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == "":
                return False
    return True


def highlight(cells):
    for cell in cells:
        cell.config(bg="lightgreen")


def disable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")


def enable_buttons():
    global game_active
    game_active = True
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="normal", text="", bg="lightblue")


def update_score():
    score_label.config(text=f"Счёт: X = {score['X']} | O = {score['O']}")


def reset_match():
    global score, game_active
    score = {"X": 0, "O": 0}
    update_score()
    enable_buttons()
    messagebox.showinfo("Новая игра", "Игра началась заново до 3 побед!")
    game_active = True


def on_click(row, col):
    global current_player, game_active

    if not game_active:
        return

    if buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player

    if check_winner():
        score[current_player] += 1
        update_score()
        disable_buttons()
        if score[current_player] >= target_wins:
            game_active = False
            messagebox.showinfo("Игра окончена", f"Игрок {current_player} выиграл матч со счётом {score[current_player]}!")
        else:
            messagebox.showinfo("Партия окончена", f"Игрок {current_player} победил!")
        return

    if check_draw():
        messagebox.showinfo("Партия окончена", "Ничья!")
        disable_buttons()
        return

    current_player = "O" if current_player == "X" else "X"


def choose_symbol(symbol):
    global current_player
    current_player = symbol
    start_frame.pack_forget()
    game_frame.pack()
    update_score()


# --- интерфейс ---
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("350x420")
window.configure(bg="white")

# стартовое меню выбора символа
start_frame = tk.Frame(window, bg="white")
tk.Label(start_frame, text="Выберите символ:", font=("Arial", 16), bg="white").pack(pady=10)
tk.Button(start_frame, text="Играть за X", font=("Arial", 14), bg="lightblue", command=lambda: choose_symbol("X")).pack(pady=5)
tk.Button(start_frame, text="Играть за O", font=("Arial", 14), bg="lightblue", command=lambda: choose_symbol("O")).pack(pady=5)
start_frame.pack()

# игровое поле
game_frame = tk.Frame(window, bg="white")

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=("Arial", 20), width=5, height=2,
                        bg="lightblue", command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

# нижняя панель с кнопками и счётом
score_label = tk.Label(game_frame, text="Счёт: X = 0 | O = 0", font=("Arial", 14), bg="white")
score_label.grid(row=3, column=0, columnspan=3, pady=10)

reset_button = tk.Button(game_frame, text="Сброс матча", font=("Arial", 12), bg="salmon", command=reset_match)
reset_button.grid(row=4, column=0, columnspan=3, pady=10)

window.mainloop()
