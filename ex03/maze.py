import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")
    
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.place(x=0, y=0)
    
    tori = tk.PhotoImage(file="pra03/fig/9.png")
    cx, cy = 300, 400
    canvas.create_image(cx, cy, image=tori, tags="tori")
    
    root.mainloop()