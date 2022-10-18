import tkinter as tk
import tkinter.messagebox as tkm

def key_down(event):
    global key
    key = event.keysym
    #tkm.showinfo("キー押下", f"{key}キーが押されました")
    
def key_up(event):
    global key
    key = ""
    
def main_proc():    
    global cx, cy, key, canvas
    if key == "Up":
        cy -= 20
    elif key == "Down":
        cy += 20
    elif key == "Left":
        cx -= 20
    elif key == "Right":
        cx += 20
        
    canvas.coords(bird, cx, cy)
    
    root.after(50, main_proc)
    
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")
    
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.place(x=0, y=0)
    
    tori = tk.PhotoImage(file="pra03/fig/9.png")
    cx, cy = 300, 400
    bird = canvas.create_image(cx, cy, image=tori, tags="tori")
    
    key = ""
    
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()
    
    root.mainloop()