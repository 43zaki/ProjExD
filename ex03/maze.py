import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker
import random

def key_down(event):
    global key
    key = event.keysym
    #tkm.showinfo("キー押下", f"{key}キーが押されました")
    
def key_up(event):
    global key
    key = ""
    
def main_proc():    
    global cx, cy, canvas, mx, my, key, ex, ey
    enemy_move()#enemyを動かす
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
        maze_source[ey][ex] = 0
        key = ""
        mx, my = 1, 1 #mx, myの初期化
        ex, ey = len(maze_source[0])-2, len(maze_source)-2 #ex, eyの初期化 
        tkm.showinfo("ゴール達成", "GOAL")
    elif maze_source[my][mx] == 4:#敵と同じ場所にいるなら
        maze_source[ey][ex] = 0
        key = ""
        mx, my = 1, 1 #mx, myの初期化
        ex, ey = len(maze_source[0])-2, len(maze_source)-2 #ex, eyの初期化 
        tkm.showinfo("敵との遭遇", "GAME OVER")
    
    root.after(50, main_proc)
    
def enemy_move(): #enemyを動かす関数
    global maze_source, canvas, enemy, ex, ey, ecx, ecy
    x, y, ms= ex, ey, maze_source[ey][ex]
    move = random.choice(["Up", "Down", "Left", "Right"])
        
    if move == "Up":
        #cy -= 100
        ey -= 1
    elif move == "Down":
        #cy += 100
        ey += 1
    elif move == "Left":
        #cx -= 100
        ex -= 1
    elif move == "Right":
        #cx += 100
        ex += 1
        
    if maze_source[ey][ex] == 0 or maze_source[ey][ex] == 2:
        ecx = ex*100+50
        ecy = ey*100+50
        canvas.coords(enemy, ecx, ecy)
        if ms == 3:
            maze_source[y][x] = 3
        else:
            maze_source[y][x] = 0
        maze_source[ey][ex] = 4
    elif maze_source[ey][ex] == 3:
        ecx = ex*100+50
        ecy = ey*100+50
        canvas.coords(enemy, ecx, ecy)
        maze_source[y][x] = 0
        maze_source[ey][ex] = 3
    else:
        ex = x
        ey = y
    
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")
    
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.place(x=0, y=0)
    
    maze_source = maze_maker.make_maze(15, 9)
    maze_maker.show_maze(canvas, maze_source)
    
    tori = tk.PhotoImage(file="ex03/fig/9.png")
    cx, cy = 300, 400
    mx, my = 1, 1
    bird = canvas.create_image(cx, cy, image=tori, tags="tori")
    
    enemy_photo = tk.PhotoImage(file="ex03/fig/5.png") #enemy画像を描画
    ex, ey = len(maze_source[0])-2, len(maze_source)-2
    ecx, ecy = 0, 0 
    enemy = canvas.create_image(ecx, ecy, image=enemy_photo, tags="enemy")
    
    key = ""
    
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()
    
    root.mainloop()