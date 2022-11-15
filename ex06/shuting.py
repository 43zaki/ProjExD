import sys
from random import randint

import pygame as pg


class Screen: # スクリーンと背景を生成するクラス　　 
    def __init__(self, title, wh_pos:tuple, file_path):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh_pos)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file_path)
        self.bgi_rct = self.bgi_sfc.get_rect()
        # 画面のスクロール設定
        self.scroll = 0
        self.scroll_speed = -3
        self.x = 0
        self.y = 0
        # 0と画面縦サイズの二つをリストに入れておく
        self.imagesize = [0,900]
        
    def update(self):
        # for文で２つの位置に１枚づつバックグラウンドを描画する（描画するx位置は上で指定したimagesizeリスト）
        for i in range(2):
            self.sfc.blit(self.bgi_sfc, (self.x, self.scroll - self.imagesize[i]))
        self.scroll -= self.scroll_speed
        # 画像が端まで来たら初期位置に戻す
        if abs(self.scroll) > 900:
            self.scroll = 0
            
            
class Prayer(pg.sprite.Sprite): # prayerが動かす挙動を設定するクラス
    key_delta = {
        pg.K_UP:    [0, -3],
        pg.K_DOWN:  [0, +3],
        pg.K_LEFT:  [-3, 0],
        pg.K_RIGHT: [+3, 0],
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
                
                
class Shot(pg.sprite.Sprite): # 球に関するクラス
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
        

class Enemy(pg.sprite.Sprite): # enemyに関するクラス
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
        

class Item(pg.sprite.Sprite): # アイテムを生成するクラス　山崎
    def __init__(self, file_path1, size, first_pos:tuple, speed:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path1)
        self.image = pg.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect()
        self.rect.center = first_pos
        self.vx = speed[0]
        self.vy = speed[1]
        
    def update(self,scrn):
        self.rect.move_ip(self.vx, self.vy)
        
        
class Thunder(pg.sprite.Sprite): # 雷（無敵状態）を生成するクラス　山崎
    def __init__(self, file_path1, size, first_pos:tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path1)
        self.image = pg.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect()
        self.rect.center = first_pos
        
    def update(self, scrn=None, vx=0, vy=0):
        self.rect.move_ip(vx, vy)
        

class BulletCount(pg.sprite.Sprite): # 弾丸の弾数を表示するクラス　山崎
    def __init__(self, bullet=100):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = "white"
        self.bullet = bullet
        self.update()
        self.rect = self.image.get_rect().move(10, 860)
        
    def update(self, scrn=None, add_bullet=0):
        self.bullet += add_bullet
        msg = "Bullet: %d" % self.bullet
        self.image = self.font.render(msg, 0, self.color) 
        
        
class Score(pg.sprite.Sprite): # スコアの表示を生成するクラス　山崎
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

class Deta: #ハイスコア用Txtの変更　布施
    def __init__(self):
        self.highscore = 0  #ハイスコアの初期化
    
    def Load(self,filepass):
        with open(filepass ,'r',encoding="utf8") as f:
            try:
                self.highscore=int(f.read())#データがあればそれをハイスコアとする
            except:
                self.highscore=0            #無ければハイスコアを0とする
    
    def update(self,filepass,hiscore):      #hightscoreの更新
        with open(filepass ,'w',encoding="utf8") as f:
            f.write(str(hiscore))
    
    def reset(self,filepass):              #hightscoreのリセット
        with open(filepass ,'w',encoding="utf8") as f:
            f.write("")


class Screen_st:       #動かないスクリーン用　布施
    def __init__(self,title,wh,bgfile):
        pg.display.set_caption(title)               #スクリーンのタイトル設定
        self.scrn_sfc=pg.display.set_mode(wh)       #スクリーン用sfc
        self.scrn_rect=self.scrn_sfc.get_rect()     #スクリーン用Rect
        self.bg_sfc =pg.image.load(bgfile)     #背景Sfc
        self.bg_rect=self.bg_sfc.get_rect()         #背景Rect 
    
    def blit(self):
        self.scrn_sfc.blit(self.bg_sfc,self.bg_rect)    #スクリーンの描画
        return self.scrn_sfc

# png=["fig/0.png","fig/1.png","fig/2.png"]
# toriping=0

class Bird:           #画像読み込み、表示　布施
    def __init__(self,filename,bairitu,syokiiti):
        self.gazou_sfc=pg.image.load(filename)     #画像用のSfcの作成
        self.gazou_sfc= pg.transform.rotozoom(self.gazou_sfc, 0, bairitu)   #画像の選択と倍率の設定
        self.gazou_rect=self.gazou_sfc.get_rect()   #画像用のRect作成
        self.gazou_rect.center=(syokiiti)           #画像の位置を設定
    
    def blit(self,sc):
        sc.blit(self.gazou_sfc,self.gazou_rect) #渡されたスクリーンSfcに画像の描画


class Font:            #文字表示用　布施
    def __init__(self,size,Non=None):   #第一引数にフォントサイズ　第二引数にフォントの設定
        self.word=pg.font.Font(Non,size)    #フォントとサイズの設定　第二引数が無ければNoneを返しデフォルトフォントfreesansbold.ttfを使用
        
    def brit(self,sc,syokiiti,word,colour): #第一引数に描画する背景sfc、第二に位置（x、y）、第三に表示する文字、第四に色（R,G,B）
        self.word_sfc=self.word.render(f"{word}",True,colour)   #テキストの設定
        sc.blit(self.word_sfc,syokiiti) #背景sfcに描画

        

           
def main():
    global mod ,sco
    sco=0  #今回の得点用
    hiscore=Deta()  #ハイスコアの読み込み
    font=Font(50)   #ハイスコア表示用
    hiscore.Load("ex06\data\Highscore.txt")
    start = 0 # 無敵時間のスタートの初期値
    item_time = 0 # 無敵時間の初期値 エラーを起こさないため
    bullet = 50 # playerが撃てる弾数
    
    scrn = Screen("進撃のこうかとん", (1600, 900), "ex06/data/bg.jpg")
    player = Prayer("ex06/data/sentou.png", 0.3, (800, 830))
    enemy = Enemy("ex06/data/6.png", 1.5, (100, 70), (5 , 1))
    score = Score()
    bullet_count = BulletCount(bullet=bullet)
    thunder = None # エラーを起こさないため
    
    enemy_grp_dct = {} # enemyのグループの辞書を作成
    
    player_grp = pg.sprite.Group(player) # playerに関するグループを作成する
    enemy_grp1 = pg.sprite.Group(enemy) # enemyに関するグループを作成する
    enemy_grp2 = pg.sprite.Group() # enemyの弾丸に関するグループを作成する
    enemy_grp3 = pg.sprite.Group() # boss_enemyに関するグループを作成する
    thunder_item_grp = pg.sprite.Group() # thunder_itemに関するグループを作成する
    bullet_item_grp = pg.sprite.Group() # bulletr_itemに関するグループを作成する
    group = pg.sprite.Group(player, enemy, bullet_count, score) # 全ての動きにに関するグループを作成する
    
    # enemyのグループに対するスコア
    enemy_grp_dct[enemy_grp1] = 300 # 通常の敵
    enemy_grp_dct[enemy_grp2] = 100 # 敵の弾丸
    enemy_grp_dct[enemy_grp3] = 1000 # ボス
    
    pg.time.set_timer(30, 1500) # 1.5秒ごとに敵が生成される
    pg.time.set_timer(31, 3000) # 3.0秒ごとに敵の弾丸が生成される
    pg.time.set_timer(32, 10000) # 10秒ごとに雷のアイテムが生成される
    pg.time.set_timer(33, 7000) # 5.0秒ごとに弾丸のアイテムが生成される
    pg.time.set_timer(34, 15000) # 15秒ごとにボスが生成される
    
    clock = pg.time.Clock()
    
    while True:
        scrn.update()
        group.update(scrn.sfc)
        group.draw(scrn.sfc)
        font.brit(scrn.sfc,[1300,10],f"Highscore: {hiscore.highscore}",(255,0,0))   #ハイスコアの表示
        
        if pg.sprite.spritecollide(player, thunder_item_grp , dokill=True):
            # playerが雷のアイテムと接触したとき、
            # playerの周りで雷が発生し無敵になる
            start = pg.time.get_ticks()
            item_time = 3000 # 無敵になる時間
            x = player.rect.centerx # 雷の画像のx座標
            y = player.rect.centery # 雷の画像のy座標
            prcx = player.rect.centerx # playerと一緒に画像を更新するためにplayerの位置を保存
            prcy = player.rect.centery # playerと一緒に画像を更新するためにplayerの位置を保存
            thunder = Thunder("ex06/data/thunder.png", 1, (x, y))
            group.add(thunder)
            player_grp.add(thunder)

        if pg.sprite.spritecollide(player, bullet_item_grp , dokill=True):
            # playerが弾丸のアイテムと接触したとき、
            # playerの弾丸数が増える
            add_bullet = 5
            bullet += add_bullet
            bullet_count.update(add_bullet=add_bullet)
            
        for enemy_grp, add_score in enemy_grp_dct.items(): # enemy_grp: enemyのグループ名, add_score: enemyのスコア
            finish = pg.time.get_ticks()
            going = True # playerとenemyのグループが衝突したときにplayerのグループが消えるかを判定する。True:消える, False:消えない
            if finish-start < item_time:
                # 無敵時間内の雷の座標の更新
                thunder_x = player.rect.centerx-prcx
                thunder_y = player.rect.centery-prcy
                prcx = player.rect.centerx
                prcy = player.rect.centery
                thunder.update(vx=thunder_x, vy=thunder_y)
                going = False
            elif group.has(thunder):
                # 無敵状態でないときに、雷がグループ内にあるとき雷をグループから削除する
                group.remove(thunder)
                player_grp.remove(thunder)
            elif pg.sprite.spritecollide(player, enemy_grp , dokill=False): 
                # playerとenemyが衝突したら終了
                mod=2
                return
            if pg.sprite.groupcollide(player_grp, enemy_grp, dokilla=going, dokillb=True):
                # playerの弾丸と敵が衝突したときにスコアを更新する
                score.update(add_score=add_score) 
                sco=score.score
                
                
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                before = pg.time.get_ticks()
            if event.type == pg.KEYUP and event.key == pg.K_SPACE and bullet > 0:
                # スペースが押されてplayerの弾数が残っているときこうかとんから弾丸が発射される
                after = pg.time.get_ticks()
                charge = 10 + (after - before)//40 # 弾丸の大きさを決める
                if charge > 100: # 弾丸の半径が100よりも大きかったら100に固定する
                    charge = 100
                x = player.rect.centerx
                y = player.rect.centery
                shot = Shot((255, 0, 0), charge, (0, -4), (x, y))
                group.add(shot)
                player_grp.add(shot)
                add_bullet = -1 # 弾数を減らす
                bullet += add_bullet
                bullet_count.update(add_bullet=add_bullet)
            if event.type == 30:
                # 1.5秒経ったときenemyを生成する。
                enemyx = randint(100, 1500)
                spdx = randint(-5, 5)
                enemy = Enemy("ex06/data/6.png", 1.5, (enemyx, 70), (spdx, 1))
                group.add(enemy)
                enemy_grp1.add(enemy)
            if event.type == 31:
                # 3.0秒経ったときenemyから弾丸を生成する。
                x = enemy.rect.centerx
                y = enemy.rect.centery
                shot = Shot((0, 255, 0), 10, (0, 4), (x, y))
                group.add(shot)
                enemy_grp2.add(shot)
            if event.type == 32:
                # 10.0秒経ったとき雷アイテムを生成する
                x = randint(10, 1590)
                y = 10
                item = Item("ex06/data/thunder01.png", 0.1, (x, y), (0, 1))
                group.add(item)
                thunder_item_grp.add(item)
            if event.type == 33:
                # 7.0秒経ったとき弾丸アイテムを生成する
                x = randint(10, 1590)
                y = 10
                item = Item("ex06/data/bullet.png", 0.2, (x, y), (0, 1))
                group.add(item)
                bullet_item_grp.add(item)
            if event.type == 34:
                # 15.0秒ごとにboss_enemyを生成する。
                enemyx = randint(100, 1500)
                boss_enemy = Enemy("ex06/data/6.png", 0.5, (enemyx, 70), (10, 0))
                group.add(boss_enemy)
                enemy_grp3.add(boss_enemy)
                 
        pg.display.update() 
        clock.tick(200)

def main2 ():               #スタート画面　布施
    global mod 
    score=Deta()
    score.Load("ex06\data\Highscore.txt")   #ハイスコアの読み込み
    pg.init()
    scrn_sfc=Screen_st("進撃のこうかとん",(1600,900),"ex06/data/bg.jpg")    #背景Sfccの作成
    bird=Bird("ex06/data/6.png",3.0,(800,450))  #鳥Sfcの作成
    font=Font(80)   #フォントサイズ80の準備
    font1=Font(100) #フォントサイズ100の準備
    font2=Font(150,"SoukouMincho.ttf")#フォントの設定とサイズの設定　フォントはSoukouMincho.ttfを指定
    keikoku=Bird("ex06/data/keikoku.jpg",1.0,(800,450)) 
    ans=0


    while True:
        nsc=scrn_sfc.blit()
        bird.blit(nsc)
        font.brit(nsc,[10,10],f"Highscore: {score.highscore}",(255,255,255))
        font1.brit(nsc,[500,600],f"[S] : Start",(255,255,255))
        font1.brit(nsc,[500,700],f"[C] : Clear high score",(255,255,255))
        font2.brit(nsc,[200,150],"進撃のこうかとん",(255,255,255))
        
        
        if ans==1:
            keikoku.blit(nsc)       #ans=1の時警告画面が出るようにする
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
        pressed = pg.key.get_pressed()
        if pressed[pg.K_s]: #Sが押されたらmod=1にしゲーム画面に移行する
            mod=1
            return
        if pressed[pg.K_c]: #Cが押されたらansを１にし警告画面が出るようにする
            ans=1
        
        if ans==1 and pressed[pg.K_y]:          #警告画面が出ているときにYを押すと
            score.reset("ex06\data\Highscore.txt")  #ハイスコアを初期化し表示しなおす
            ans=0
            return
        
        if ans==1 and pressed[pg.K_n]:   #警告画面が出ているときにNを押すとans=0にし警告画面を非表示
            ans=0
        pg.display.update()

def main3 ():              #GameOver画面　布施
    global mod,sco
    score=Deta()
    score.Load("ex06\data\Highscore.txt")   #ハイスコアの読み込み
    pg.init()
    scrn_sfc=pg.display.set_mode((1600,900))    #スクリーン用Sfcの作成
    pg.display.set_caption("Game Over")
    font=Font(200)      #フォントサイズ200の準備
    font1=Font(100)     #フォントサイズ100の準備
    
    while True:
        if score.highscore< sco:    #もし今回の得点がハイスコアより高かったら
            score.update("ex06\data\Highscore.txt",sco)     #ハイスコアを今回の得点で更新
            font1.brit(scrn_sfc,[500,450],f"HighScore: {sco}",(255,0,0))    #ハイスコアと赤で表示
        
        else:   #ハイスコア以下なら
            font1.brit(scrn_sfc,[600,450],f"Score: {sco}",(255,255,255)) #スコアと白で表示
        
        font.brit(scrn_sfc,[400,200],f"Game Over",(255,255,255))    #テキストの表示
        font1.brit(scrn_sfc,[500,650],f"[R] : Rstert",(255,255,255))     
        font1.brit(scrn_sfc,[500,750],f"[E] : Exit",(255,255,255))    
        
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pressed = pg.key.get_pressed()  
        if pressed[pg.K_r]:  #Rが押されたらmod=0にしスタート画面へ
            mod=0
            return
        if pressed[pg.K_e]: #Eが押されたらプログラムの終了
            pg.quit()
            sys.exit()

        
if __name__ == "__main__":
    mod=0
    sco=0
    pg.init() # 初期化
    while True:
        if mod==0:  #スタート画面
            main2()
        if mod==1:  #ゲーム画面
            main()   # ゲームの本体
        if mod==2:  #GameOver画面
            main3()#
    pg.quit() # 初期化の解除
    sys.exit()