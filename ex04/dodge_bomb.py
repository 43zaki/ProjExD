import pygame as pg
import sys
import random

def main():
    pg.init()
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    bgimg = pg.image.load("ex04/fig/pg_bg.jpg")
    loop = True
    
    
    
    while loop:
        clock = pg.time.Clock()
        clock.tick(1000)
        pg.display.update()
        
        scrn_sfc.blit(bgimg, (0,0))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:loop = False
            
    pg.quit()
    sys.exit()
    
    
    
if __name__ == "__main__":
    main()