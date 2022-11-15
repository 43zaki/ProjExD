import pygame as pg
import sys
from random import randint, choice

class Screen(pg.sprite.Sprite): #スクリーンと背景を生成するクラス　　 
    def __init__(self, title, wh_pos:tuple, file_path):
        pg.sprite.Sprite.__init__(self)
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh_pos)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file_path)
        self.bgi_rct = self.bgi_sfc.get_rect()
        
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)
    
        
class Bird(pg.sprite.Sprite): #こうかとんを生成するクラス
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
        self.judge = 0
     
    def blit(self, scrn):
        scrn.blit(self.image, self.rect)
        
    def update(self, scrn):
        key_states = pg.key.get_pressed()
        rct = scrn.get_rect()
        for key, delta in self.key_delta.items():
            if key_states[key]:
                if key_states[pg.K_LEFT] and self.judge == 1:
                    self.image = pg.transform.flip(self.image, 1, 0)
                    self.judge -= 1
                elif key_states[pg.K_RIGHT] and self.judge == 0:
                    self.image = pg.transform.flip(self.image, 1, 0)
                    self.judge += 1
                self.rect.move_ip(delta[0], delta[1])
                if check_bound(self.rect, rct) != (+1, +1):
                    self.rect.move_ip(-1*delta[0], -1*delta[1])
                scrn.blit(self.image, self.rect)
                
               
class Bomb(pg.sprite.Sprite): # 爆弾を生成するクラス
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
          
          
class Sword(pg.sprite.Sprite): # 剣を生成するクラス
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
        }
    
    def __init__(self, file_path, size, first_pos:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path)
        self.image = pg.transform.rotozoom(self.image, 0, size)
        self.image = pg.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect.center = first_pos
        self.judge = 1 #こうかとんがどちらの向きに向いているかジャッジする。右だと1左だと－1
    
    def update(self, scrn):
        key_states = pg.key.get_pressed()
        rct = scrn.get_rect()
        for key, delta in self.key_delta.items():
            if key_states[key]:
                if key_states[pg.K_LEFT] and self.judge == -1: #こうかとんが右を向いているときに
                    self.image = pg.transform.flip(self.image, 1, 0)
                    self.judge = 1
                    self.rect.move_ip(-160, 0)
                elif key_states[pg.K_RIGHT] and self.judge == 1:
                    self.image = pg.transform.flip(self.image, 1, 0)
                    self.judge = -1
                    self.rect.move_ip(160, 0)
                self.rect.move_ip(delta[0], delta[1])
                if check_bound(self.rect, rct) != (+1, +1):
                    self.rect.move_ip(-1*delta[0], -1*delta[1])
                scrn.blit(self.image, self.rect)
                
# class HP(pg.sprite.Sprite):
#     def __init__(self, x, y, width, max):
#         pg.sprite.Sprite.__init__(self)
#         self.x = x
#         self.y = y
#         self.width = width
#         self.max = max # 最大HP
#         self.hp = max # HP
#         self.mark = int((self.width - 4) / self.max) # HPバーの1目盛り

#         self.font = pg.font.SysFont(None, 28)
#         self.label = self.font.render("HP", True, (255, 255, 255))
#         self.frame = Rect(self.x + 2 + self.label.get_width(), self.y, self.width, self.label.get_height())
#         self.bar = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)
#         self.value = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)

#     def update(self, scrn):
#         self.value.width = self.hp * self.mark
#         pg.draw.rect(scrn, (255, 255, 255), self.frame)
#         pg.draw.rect(scrn, (0, 0, 0), self.bar)
#         pg.draw.rect(scrn, (0, 0, 255), self.value)
#         scrn.blit(self.label, (self.x, self.y))
        
        
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
    scrn = Screen("戦う！こうかとん", (1600, 900), "pra05/fig/pg_bg.jpg")
    bird = Bird("pra05/fig/6.png", 2, (900, 400))
    sword = Sword("pra05/fig/sword.png", 0.15, (820, 350))
    # hp = HP(900, 400, 100, 100)
    bomb_lst = []
    for _ in range(5): #爆弾を5回生成
        x = choice([+1, -1])
        y = choice([+1, -1])
        bomb = Bomb((255, 0, 0), 10, (x, y))
        bomb_lst.append(bomb)
    
    bird_grp = pg.sprite.Group(bird)
    bomb_grp = pg.sprite.Group(*bomb_lst)
    sword_grp = pg.sprite.Group(sword)
    groop = pg.sprite.Group(bird, *bomb_lst, sword)
    pg.time.set_timer(30, 8000) #8秒ごとに爆弾を生成
    
    clock = pg.time.Clock() 
    while True:
        scrn.blit()
        groop.update(scrn.sfc)
        groop.draw(scrn.sfc)
        # hp.draw(scrn.sfc)
                
        if pg.sprite.groupcollide(bird_grp, bomb_grp, dokilla=True, dokillb=True):
            return       
        
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                sword.rect.move_ip(0, 90)
                sword.image = pg.transform.rotate(sword.image, 90*sword.judge)
                if pg.sprite.groupcollide(sword_grp, bomb_grp, dokilla=False, dokillb=True):
                    pass
            if event.type == pg.KEYUP and event.key == pg.K_SPACE:
                sword.rect.move_ip(0, -90)
                sword.image = pg.transform.rotate(sword.image, -90*sword.judge)
                if pg.sprite.groupcollide(sword_grp, bomb_grp, dokilla=False, dokillb=True):
                    pass
            if event.type == pg.QUIT:
                return
            if event.type == 30:
                bomb = Bomb((255, 0, 0), 10, (x, y))
                groop.add(bomb)
                bomb_grp.add(bomb)
                
        
        pg.display.update() 
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化 
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
