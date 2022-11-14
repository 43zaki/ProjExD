import sys
from random import choice, randint

import pygame as pg


class Screen: #スクリーンと背景を生成するクラス　　 
    def __init__(self, title, wh_pos:tuple, file_path):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh_pos)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file_path)
        self.bgi_rct = self.bgi_sfc.get_rect()
        #画面のスクロール設定
        self.scroll = 0
        self.scroll_speed = -3
        self.x = 0
        self.y = 0
        #0と画面縦サイズの二つをリストに入れておく
        self.imagesize = [0,900]
        
    def update(self):
        #for文で２つの位置に１枚づつバックグラウンドを描画する（描画するx位置は上で指定したimagesizeリスト）
        for i in range(2):
            self.sfc.blit(self.bgi_sfc, (self.x, self.scroll - self.imagesize[i]))
        self.scroll -= self.scroll_speed
        #画像が端まで来たら初期位置に戻す
        if abs(self.scroll) > 900:
            self.scroll = 0
            
            
class Prayer(pg.sprite.Sprite): #prayerが動かす挙動を設定するクラス
    key_delta = {
        pg.K_UP:    [0, -2],
        pg.K_DOWN:  [0, +2],
        pg.K_LEFT:  [-2, 0],
        pg.K_RIGHT: [+2, 0],
        }
    
    def __init__(self, file_path1, size, first_pos:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path1)
        self.image = pg.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect()
        self.rect.center = first_pos
        
    def update(self, scrn):
        key_states = pg.key.get_pressed()
        rct = scrn.get_rect()
        for key, delta in self.key_delta.items():
            if key_states[key]:
                self.rect.move_ip(delta[0], delta[1])
                if check_bound(self.rect, rct) != (+1, +1):
                    self.rect.move_ip(-1*delta[0], -1*delta[1])
                
                
class Shot(pg.sprite.Sprite): #球に関するクラス
    def __init__(self, color:tuple, radius, speed:tuple, pos:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((2*radius, 2*radius)) # 空のSurface
        self.image.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.image, color, (radius, radius), radius) # 爆弾用の円を描く
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.vx = speed[0]
        self.vy = speed[1]
    
    def update(self, scrn):
        self.rect.move_ip(self.vx, self.vy)
        

class Enemy(pg.sprite.Sprite): #enemyに関するクラス
    def __init__(self, file_path1, size, first_pos:tuple, speed:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path1)
        self.image = pg.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect()
        self.rect.center = first_pos
        self.vx = speed[0]
        self.vy = speed[1]
        
    def update(self, scrn):
        rect = scrn.get_rect()
        yoko = +1
        if self.rect.left < rect.left or rect.right < self.rect.right: 
            yoko = -1
        self.vx *= yoko
        self.rect.move_ip(self.vx, self.vy)
        
        
class Score(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 50)
        self.font.set_italic(1)
        self.color = "white"
        self.score = 0
        self.update()
        self.rect = self.image.get_rect().move(10, 10)
        
    def update(self, scrn=None, add_score=0):
        self.score += add_score  
        msg = "Score: %d" % self.score
        self.image = self.font.render(msg, 0, self.color) 
        
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
    scrn = Screen("進撃のこうかとん", (1600, 900), "ex06/data/bg.jpg")
    player = Prayer("ex06/data/sentou.png", 0.3, (800, 830))
    enemy = Enemy("pra05/fig/6.png", 1.5, (100, 70), (5 , 1))
    score = Score()
    
    enemy_grp_dct = {} #enemyのグループの辞書を作成
    
    player_grp = pg.sprite.Group(player) #playerに関するグループを作成する
    enemy_grp1 = pg.sprite.Group(enemy) #enemyに関するグループを作成する
    enemy_grp2 = pg.sprite.Group() #enemyの球に関するグループを作成する
    group = pg.sprite.Group(player, enemy, score) #全ての動きにに関するグループを作成する
    
    #enemyのグループに対するスコア
    enemy_grp_dct[enemy_grp1] = 100
    enemy_grp_dct[enemy_grp2] = 500
    
    pg.time.set_timer(30, 1500) #1.5秒ごとに敵が生成される
    pg.time.set_timer(31, 1000) #1秒ごとに敵の球が生成される
    
    clock = pg.time.Clock()
    
    while True:
        scrn.update()
        group.update(scrn.sfc)
        group.draw(scrn.sfc)
        
    
        for enemy_grp, add_score in enemy_grp_dct.items():
            if pg.sprite.spritecollide(player, enemy_grp , dokill=False): 
                return
            if pg.sprite.groupcollide(player_grp, enemy_grp, dokilla=True, dokillb=True):
                score.update(add_score=add_score) 
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # スペースが押されたときにこうかとんから球が発射される
                x = player.rect.centerx
                y = player.rect.centery
                shot = Shot((255, 0, 0), 13, (0, -4), (x, y))
                group.add(shot)
                player_grp.add(shot)
            if event.type == 30:
                # 1.5秒経ったときenemyを生成する。
                enemyx = randint(100, 1500)
                spdx = randint(-5, 5)
                enemy = Enemy("pra05/fig/6.png", 1.5, (enemyx, 70), (spdx, 1))
                group.add(enemy)
                enemy_grp1.add(enemy)
            if event.type == 31:
                # 1.0秒経ったときenemyから球を生成する。
                x = enemy.rect.centerx
                y = enemy.rect.centery
                shot = Shot((0, 255, 0), 10, (0, 3), (x, y))
                group.add(shot)
                enemy_grp2.add(shot)
                 
        pg.display.update() 
        clock.tick(200)
        
if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()