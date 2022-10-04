import tkinter as tk
import tkinter.messagebox as tkm

def click_number(event):
    btn = event.widget
    num = btn["text"]
    #tkm.showinfo(f"{num}", f"{num}のボタンが押されました")
    entry.insert(tk.END, num) #練習5
    
def click_equal(event):
    eqn = entry.get()
    eqn = eqn.replace("÷", "/")
    eqn = eqn.replace("×", "*")
    res = eval(eqn)
    entry.delete(0, tk.END)
    entry.insert(tk.END, res)
    
def click_del(event):
    dln = entry.get()
    dln = dln[0:-1]
    entry.delete(0, tk.END)
    entry.insert(tk.END, dln)

root = tk.Tk()
root.geometry("400x500")

entry = tk.Entry(root, width=10, font=(", 40"), justify="right") # 練習4
entry.grid(row=0, column=0, columnspan=3)


r, c = 1, 0
shousu = ["."]
numbers = list(range(9, -1, -1))
for i, num in enumerate(numbers+shousu, 1):
    btn = tk.Button(root, text=f"{num}", font=("", 30), width=4, height=2)
    btn.bind("<1>", click_number)
    btn.grid(row=r, column=c)
    c += 1
    if i%3 == 0:
        r += 1
        c = 0

operators = ["×", "÷", "-", "+"]
for i, ope in enumerate(operators, 1):
    btn = tk.Button(root, text=f"{ope}", font=("", 30), width=4, height=2)
    btn.bind("<1>", click_number)
    btn.grid(row=i, column=3)

btn_eq = tk.Button(root, text="=", font=("", 30), width=4, height=2)
btn_eq.bind("<1>", click_equal)
btn_eq.grid(row=4, column=2)

btn_dl = tk.Button(root, text="☜×", font=("", 30), width=4, height=1)
btn_dl.bind("<1>", click_del)
btn_dl.grid(row=0, column=3)


        
root.mainloop()
    