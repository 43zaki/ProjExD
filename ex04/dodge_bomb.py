import pygame as pg
import sys
import random

def main():
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    bgimg = pg.image.load("ex04/fig/pg_bg.jpg")
    loop = True #実行し続けるかどうかを判定する
    tori_x = 900
    tori_y = 400
    move_x, move_y = 1, 1
    x, y = 0, 0
    vx = random.randint(10, 800-10) #vxとvyは爆弾の初期位置
    vy = random.randint(10, 900-10)
    transmittance = 255 #透過率を表す
    cookie_j = 0 #クッキーがあるかないか特定
    pg.time.set_timer(30, 8000) #8秒経ったらクッキーを生成する
    
    
    
    while loop:
        
        clock.tick(1000)
        pg.display.update()
        
        
        scrn_sfc.blit(bgimg, (0,0))
        
        #こうかとん生成
        tori_sfc = pg.image.load("ex04/fig/9.png")
        tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2)
        tori_sfc.set_alpha((transmittance))
        tori_rct = tori_sfc.get_rect()
        tori_rct.center = tori_x, tori_y
        scrn_sfc.blit(tori_sfc, tori_rct)
        
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_DOWN] and tori_rct.bottom+1 < 900:
            y = tori_y #yとxは今の画像の座標を保存する
            tori_y += 10
        elif pressed_keys[pg.K_UP] and tori_rct.top-1 > 0:
            y = tori_y
            tori_y -= 10
        elif pressed_keys[pg.K_LEFT] and tori_rct.left-1 > 0:
            x = tori_x
            tori_x -= 10
        elif pressed_keys[pg.K_RIGHT] and tori_rct.right+1 < 1600:
            x = tori_x
            tori_x += 10
        
        #爆弾の生成
        bomb_sfc = pg.Surface((20, 20))
        bomb_sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10) 
        bomb_rct = bomb_sfc.get_rect()
        bomb_rct.center = vx, vy
        scrn_sfc.blit(bomb_sfc, bomb_rct)   
        vx += move_x
        vy += move_y
        
        #画面の右に出たらプログラム終了、それ以外で淵に当たったら跳ね返る
        if vx+10 >= 1600:
            loop = False
        if vx-10 <= 0 :
            move_x *= -1
        if vy-10 <= 0 or vy+10 >= 900:
            move_y *= -1
            
        if cookie_j == 1: #クッキーが描画されているとき
            scrn_sfc.blit(cookie_sfc, cookie_rct)
            if tori_rct.colliderect(cookie_rct): #クッキーとこうかとんがかさなったら
                transmittance += 50
                cookie_j = 0
        
        if tori_rct.colliderect(bomb_rct): #爆弾がこうかとんとかさなったら
            #爆発の描写
            bomb1_sfc = pg.image.load("ex04/fig/bomb1.png")
            bomb1_sfc = pg.transform.rotozoom(bomb1_sfc, 0, 0.5)
            bomb1_rct = bomb1_sfc.get_rect()
            bomb1_rct.center = tori_x, tori_y
            scrn_sfc.blit(bomb1_sfc, bomb1_rct)
            pg.display.update()
            
            #爆弾に当たったら200右に移動し爆弾の速度を上げる
            tori_x += 200
            if tori_x >= x:
                move_x = abs(move_x)+0.1
                move_x *= -1
            
            #透過率を上げる
            transmittance -= 20
            if transmittance < 15:
                loop=False
                
            #爆発の画像が表示されるようにfpsを一時的に低くする。
            clock.tick(10)
            
        for event in pg.event.get():
            if event.type == pg.QUIT:loop = False
            if event.type == 30: #クッキーの生成
                cookie_j = 1 
                cx = random.randint(800, 1600)
                cy = random.randint(0, 900)
                cookie_sfc = pg.image.load("ex04/fig/cookie.png")
                cookie_sfc = pg.transform.rotozoom(cookie_sfc, 0, 0.1)
                cookie_rct =    cookie_sfc.get_rect()
                cookie_rct.center = cx, cy 
                scrn_sfc.blit(cookie_sfc, cookie_rct)
                
    pg.quit()
    sys.exit()
    
    
if __name__ == "__main__":
    main()