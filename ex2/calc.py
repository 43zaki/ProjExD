import tkinter as tk
import tkinter.messagebox as tkm

def click_number(event):
    btn = event.widget
    num = int(btn["text"])
    tkm.showinfo(f"{num}", f"{num}のボタンが押されました")


root = tk.Tk()
root.geometry("300x500")



# for i in range(9,-1,-1):
#     button = tk.Button(root, text=f"{i}", font=("Times New Roman", 30), width=4, height=2)
#     a = 0
#     b = 2
#     button.grid(a, b)
#     if b%3 == 2:
#         a += 1

r, c = 0, 0
for i, num in enumerate(range(9,-1, -1), 1):
    btn = tk.Button(root, text=f"{num}", font=("", 30), width=4, height=2)
    btn.bind("<1>", click_number)
    btn.grid(row=r, column=c)
    c += 1
    if i%3 == 0:
        r += 1
        c = 0
    