import pygame as pg
import sys
from random import randint, choice

class Screen(pg.sprite.Sprite):
    def __init__(self, title, wh_pos:tuple, file_path):
        pg.sprite.Sprite.__init__(self)
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh_pos)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file_path)
        self.bgi_rct = self.bgi_sfc.get_rect()
        
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)
    
        
class Bird(pg.sprite.Sprite):
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
        }
    
    def __init__(self, file_path1, size, first_pos:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path1)
        self.image = pg.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect()
        self.rect.center = first_pos
     
    def blit(self, scrn):
        scrn.blit(self.image, self.rect)
        
    def update(self, scrn):
        key_states = pg.key.get_pressed()
        rct = scrn.get_rect()
        for key, delta in self.key_delta.items():
            if key_states[key]:
                self.rect.move_ip(delta[0], delta[1])
                if check_bound(self.rect, rct) != (+1, +1):
                    self.rect.move_ip(-1*delta[0], -1*delta[1])
                #     self.bird_rct.centerx -= delta[0]
                #     self.bird_rct.centery -= delta[1]
                scrn.blit(self.image, self.rect)
         
                
class Bomb(pg.sprite.Sprite):
    def __init__(self, color:tuple, radius, speed:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((2*radius, 2*radius)) # 空のSurface
        self.image.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.image, color, (radius, radius), radius) # 爆弾用の円を描く
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(0+radius, 1600-radius)
        self.rect.centery = randint(0+radius, 900-radius)
        self.vx = speed[0]
        self.vy = speed[1]
    
    def blit(self, scrn):
        scrn.blit(self.image, self.rect)
        
    def update(self, scrn):
        rct = scrn.get_rect()
        yoko, tate = check_bound(self.rect, rct)
        self.vx *= yoko
        self.vy *= tate
        self.rect.move_ip(self.vx, self.vy) 
        scrn.blit(self.image, self.rect)  

def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate
        

def main():
    scrn = Screen("逃げろ！こうかとん", (1600, 900), "pra05/fig/pg_bg.jpg")
    bird = Bird("pra05/fig/6.png", 2, (900, 400))
    bomb_lst = []
    for _ in range(5):
        x = choice([+1, -1])
        y = choice([+1, -1])
        bomb = Bomb((255, 0, 0), 10, (x, y))
        bomb_lst.append(bomb)
    
    bird_grp = pg.sprite.Group(bird)
    bomb_grp = pg.sprite.Group(*bomb_lst)
    groop = pg.sprite.Group(bird, *bomb_lst)


    clock = pg.time.Clock() 
    while True:
        scrn.blit()
        groop.update(scrn.sfc)
        groop.draw(scrn.sfc)
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return
                
        if pg.sprite.groupcollide(bird_grp, bomb_grp, dokilla=True, dokillb=True):
            return
        
        pg.display.update() 
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
