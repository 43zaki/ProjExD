import random
import time

def shutudai(quiz_dic): #問題を選択して表示する関数
    quiz = random.choice(list(quiz_dic.keys()))
    print(f"問題:\n{quiz}")
    return quiz
    
def kaito(quiz, quiz_dic): #回答結果の正負を判別する関数
    time_start = time.time() #解答時間計測開始
    ans = input("答え:")
    time_end = time.time() #解答時間計測終了
    if ans in quiz_dic[quiz]:
        t = time_end - time_start
        if t <= 10: #解答時間が10秒以内であるとき
            print("正解です。とても速い.まるで光だ")
        elif 10 < t <= 20: #10~20秒以内
            print("正解だ。だがお前はまだまだ早くなれる")
        elif 20 < t <= 30: #20~30秒以内
            print("正解。だが全然遅いなまるでカタツムリだ")
        else: #30秒以上
            print("せいかい...すごく遅いぞ。調べて答えるんじゃないか")
            
    else:
        print("不正解")

if __name__ == "__main__":
    quiz_dic = {"あああ":["iii", "uuu", "eee", "ooo"],
                "かかか":["qqq", "www", "rrr", "ttt"],
                "さささ":["yyy", "ppp", "sss", "ddd"]} #問題の選択肢と答え
    quiz = shutudai(quiz_dic) #クイズの取得
    kaito(quiz, quiz_dic)
