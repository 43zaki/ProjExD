import random
import time

def shutudai(quiz_dic):
    quiz = random.choice(list(quiz_dic.keys()))
    print(f"問題:\n{quiz}")
    return quiz
    
def kaito(quiz, quiz_dic):
    time_start = time.time() #解答時間計測開始
    ans = input("答え:")
    time_end = time.time() #解答時間計測終了
    if ans in quiz_dic[quiz]:
        t = time_end - time_start
        if t <= 10:
            print("正解です。すごく速い.俺でなきゃ見逃しちゃうね")
        elif 10 < t <= 20:
            print("正解だ。だがお前はまだまだ早くなれる")
        elif 20 < t <= 30:
            print("正解。しかし全然遅いな。まるでカタツムリだ")
        else:
            print("せいかい...遅いぞ。調べて答えるんじゃないのか。")
            
    else:
        print("不正解。まだまだだね")

if __name__ == "__main__":
    quiz_dic = {"あああ":["iii", "uuu", "eee", "ooo"],
                "かかか":["qqq", "www", "rrr", "ttt"],
                "さささ":["yyy", "ppp", "sss", "ddd"]}
    quiz = shutudai(quiz_dic)
    kaito(quiz, quiz_dic)
