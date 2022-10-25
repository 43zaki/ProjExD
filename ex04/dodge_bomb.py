import pygame as pg
import sys
import random

def main():
    pg.init()
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    bgimg = pg.image.load("ex04/fig/pg_bg.jpg")
    loop = True
    tori_x = 900
    tori_y = 400
    
    
    
    while loop:
        clock = pg.time.Clock()
        clock.tick(1000)
        pg.display.update()
        
        scrn_sfc.blit(bgimg, (0,0))
        
        tori_sfc = pg.image.load("ex04/fig/9.png")
        tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2)
        tori_rct =    tori_sfc.get_rect()
        tori_rct.center = tori_x, tori_y
        scrn_sfc.blit(tori_sfc, tori_rct)
        
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_DOWN] and tori_rct.bottom+1 < 900:
            tori_y += 1
        elif pressed_keys[pg.K_UP] and tori_rct.top-1 > 0:
            tori_y -= 1
        elif pressed_keys[pg.K_LEFT] and tori_rct.left-1 > 0:
            tori_x -= 1
        elif pressed_keys[pg.K_RIGHT] and tori_rct.right+1 < 1600:
            tori_x += 1
        
        for event in pg.event.get():
            if event.type == pg.QUIT:loop = False
            
    pg.quit()
    sys.exit()
    
    
    
if __name__ == "__main__":
    main()