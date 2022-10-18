import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker

def key_down(event):
    global key
    key = event.keysym
    #tkm.showinfo("キー押下", f"{key}キーが押されました")
    
def key_up(event):
    global key
    key = ""
    
def main_proc():    
    global cx, cy, canvas, mx, my, key
    if key == "Up" and maze_source[my-1][mx] != 1:
        #cy -= 20
        my -= 1
    elif key == "Down" and maze_source[my+1][mx] != 1:
        #cy += 20
        my += 1
    elif key == "Left" and maze_source[my][mx-1] != 1:
        #cx -= 20
        mx -= 1
    elif key == "Right" and maze_source[my][mx+1] != 1:
        #cx += 20
        mx += 1
        
    cx = mx*100 + 50
    cy = my*100 + 50
    canvas.coords(bird, cx, cy)
    
    if maze_source[my][mx] == 3: #ゴールしたら
        key = ""
        mx, my = 1, 1 #mx, myの初期化
        tkm.showinfo("ゴール達成", "GOAL")
    
    
    root.after(50, main_proc)
    
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")
    
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.place(x=0, y=0)
    
    maze_source = maze_maker.make_maze(15, 9)
    maze_maker.show_maze(canvas, maze_source)
    
    tori = tk.PhotoImage(file="pra03/fig/9.png")
    cx, cy = 300, 400
    mx, my = 1, 1
    bird = canvas.create_image(cx, cy, image=tori, tags="tori")
    
    key = ""
    
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()
    
    root.mainloop()