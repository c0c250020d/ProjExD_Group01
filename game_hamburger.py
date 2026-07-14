import os
import sys
import time
import random  
import pygame as pg

WIDTH, HEIGHT = 1100, 650


zairyo = {
    1: {"name": "チーズ", "height": 30, "file_name": "cheese.png", "image": None},
    2: {"name": "ベーコン", "height": 25, "file_name": "bacon.png", "image": None}, 
    3: {"name": "肉", "height": 45, "file_name": "meet.png", "image": None},
    4: {"name": "レタス", "height": 40, "file_name": "lettuce.png", "image": None},
    5: {"name": "トマト", "height": 35, "file_name": "tomato.png", "image": None},
}

#数字キーに番号を対応させる
key_id = {
    pg.K_1: 1, pg.K_KP1: 1,
    pg.K_2: 2, pg.K_KP2: 2,
    pg.K_3: 3, pg.K_KP3: 3,
    pg.K_4: 4, pg.K_KP4: 4,
    pg.K_5: 5, pg.K_KP5: 5,
}


RECIPES = {
    1: [3], #ノーマルバーガー
    2: [3, 1, 2], #ベーコンチーズバーガー
    3: [3, 1], #チーズバーガー
    4: [5, 4], #ベジタブルバーガー
    5: [3, 1, 3, 1], #ダブルバーガー
    6: [5, 2, 3, 1, 4], #スペシャルバーガー
    7: [5, 4, 2, 5, 1, 3, 2, 4] #ハッピーバーガー
}

def get_random_recipe(): #お題となるメニューをランダムに決める
    menu_idx = random.choice(list(RECIPES))

    return menu_idx

def load_and_scale_image(file_name, target_width): #材料画像を縮小

    filepath = os.path.join("image", file_name)
    img = pg.image.load(filepath).convert_alpha()
        
    orig_width, orig_height = img.get_size()
    scale_ratio = target_width / orig_width
    new_height = int(orig_height * scale_ratio)
        
    return pg.transform.scale(img, (target_width, new_height)), new_height

def load_background_image(file_name, size): #背景画像

    filepath = os.path.join("image", file_name)
    img = pg.image.load(filepath).convert_alpha() 
    return pg.transform.scale(img, size)

def ending(screen, score):
    score_font = pg.font.SysFont("meiryo", 50)
    rank_font = pg.font.SysFont("meiryo", 120)
    speak_font = pg.font.SysFont("meiryo", 40)


    if score  <= 40:
        bg_color = (130, 130, 130)
        frame_color = (0, 190, 190)
        rank_txt = rank_font.render("★☆☆☆", True, (255, 255, 0))
        speak_txt = speak_font.render("【見習いアルバイト】", True, (0, 0, 0))
    elif score <= 80:
        bg_color = (0, 190, 190)
        frame_color = (130, 130, 130)
        rank_txt = rank_font.render("★★☆☆",True, (255, 255, 0))
        speak_txt = speak_font.render("【バイトリーダー】", True, (0, 0, 0))
    elif score <= 120:
        bg_color = (0, 220, 103)
        frame_color = (255, 195, 40)
        rank_txt = rank_font.render("★★★☆", True, (255, 255, 0))
        speak_txt = speak_font.render("【三ツ星バーガー店】", True, (0, 0, 0))
    else:
        bg_color = (255, 195, 40)
        frame_color = (0, 220, 103)
        rank_txt = rank_font.render("★★★★", True, (255, 255, 0))
        speak_txt = speak_font.render("【ハンバーガーの申し子】", True, (0, 0, 0))

    bg_img = pg.Surface((1100, 650))
    pg.draw.rect(bg_img, bg_color, pg.Rect(0, 0, 1100, 650))
    # bg_img.set_alpha(230)

    score_txt = score_font.render(f"あなたのスコアは{score}点!!", True, (0, 0, 0))

    score_rct = score_txt.get_rect()
    rank_rct =rank_txt.get_rect()
    speak_rct =speak_txt.get_rect()
    score_rct.center = 550, 200
    rank_rct.center = 550, 300
    speak_rct.center = 550, 390

    box_rect = pg.Rect(250, 150, 600, 90)
    pg.draw.rect(bg_img, (255, 255, 255), box_rect, 0)

    frame_rect = pg.Rect(80, 80, 960, 490)
    pg.draw.rect(bg_img, frame_color, frame_rect, 10)


    bg_img.blit(score_txt, score_rct)
    bg_img.blit(rank_txt, rank_rct)
    bg_img.blit(speak_txt, speak_rct)

    screen.blit(bg_img,[0,0])
    pg.display.update()
    time.sleep(3)

        
def draw_score(screen, font, score):
    "スコア機能の定義"
    score_text = font.render(f"スコア：{score}", True, (255, 255, 255))
    # 左上に背景付きでスコアを表示
    pg.draw.rect(screen, (50, 50, 50), (10, 100, 260, 50))
    screen.blit(score_text, (20, 100))

def main():
    pg.init()
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("ハンバーガー屋を経営しよう")
    clock = pg.time.Clock()
    
    font = pg.font.SysFont("meiryo", 20) #判定結果の文字用
    result_font = pg.font.SysFont("meiryo", 40) 
    finish_font = pg.font.SysFont("meiryo", 48)
    timer_font = pg.font.SysFont("meiryo", 36)  #タイマー用のフォント
    score_font = pg.font.SysFont("meiryo", 36)#スコア用フォント

 
    bg_image = load_background_image("haikei_2.jpg", (WIDTH, HEIGHT)) #背景画像の読み込み

    for ing_id, info in zairyo.items(): #材料画像を読み込み
        img, computed_height = load_and_scale_image(info["file_name"], 200)
        if img:
            zairyo[ing_id]["image"] = img
            zairyo[ing_id]["height"] = computed_height 

    #見本のハンバーガー画像読み込み
    menu_images = {}
    menu_files = {
        1: "1_nomal.png", 2: "2_baconcheese.png", 3: "3_cheese.png",
        4: "4_beji.png", 5: "5_double.png", 6: "6_special.png", 7: "7_happy.png"
    }
    for k, filename in menu_files.items():
        img = pg.image.load(f"image/{filename}")
        menu_images[k] = pg.transform.rotozoom(img, 0, 0.08)

    bans_img_top = pg.image.load("image/bans_top.png")
    bans_img_top = pg.transform.rotozoom(bans_img_top, 0, 0.08)

    # 最初のターゲットレシピをランダムに決定
    target_menu = get_random_recipe()

    make_burger = [] #積み上げている材料を保存する
    judge_result = None #判定結果用

    score = 0
    # タイマーの設定
    LIMIT_TIME = 30  #制限時間（秒）
    start_ticks = pg.time.get_ticks()  #ゲーム開始時のミリ秒を取得
    # スコアの初期値


    x = True
    while x:
        # 背景画像を描画
        if bg_image:
            screen.blit(bg_image, (0, 0))

        #タイマーの計算
        #経過時間を秒に変換し、残り時間を計算
        seconds_passed = (pg.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, LIMIT_TIME - seconds_passed)

        #残り時間を画面の左上に描画
        timer_text = timer_font.render(f"残り時間: {int(time_left)}秒", True, (255, 255, 255))
        #文字が見えやすいように背景に黒い四角形を軽く敷く
        pg.draw.rect(screen, (0, 0, 0), (15, 20, 260, 50))
        screen.blit(timer_text, (20, 20))

        #時間切れの判定（正解・不正解の演出中はタイマーで死なないようにする）
        if time_left <= 0:
            gameover = finish_font.render("TIME UP! GAME OVER", True, (200, 0, 0))
            screen.blit(gameover, (325, 300))
            pg.display.update()
            time.sleep(2)
            ending(screen, score)
            return
            
        # スコアの描画
        draw_score(screen, score_font, score)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                x = False
                
            elif event.type == pg.KEYDOWN: 
                if (judge_result == 1) or (judge_result == 2): # クリア時に何かキーを押したら次の注文へ
                # 判定が出ている（クリアorミス）時に何かキーを押したら次の注文へ
                    if judge_result is not None:
                        make_burger = []
                        judge_result = None
                        target_menu = get_random_recipe()  # 次のレシピをランダム決定
                        continue

                
                if event.key in key_id: # 数字キーに対応して具材を乗せる
                    ing_id = key_id[event.key]
                    make_burger.append(ing_id)

                elif event.key == pg.K_RETURN:# エンターキーで判定（商品提供）
                    if make_burger == RECIPES[target_menu]:
                        judge_result = 1
                        score += 10 #成功で+10点
                    else:
                        judge_result = 2
                        score = max(0, score - 10) # ミスで-10点（0未満にならない

        # ランダムに決定されたtarget_menuに合わせてモニターの位置に見本画像を置く
        if target_menu in menu_images:
            screen.blit(menu_images[target_menu], (500, 60))

        #材料の積み上げ
        base_x = 830
        base_y = 600  
        new_y = base_y       

        for index, zairyo_id in enumerate(make_burger):
            info = zairyo[zairyo_id]
            height = info["height"]
            
            if index == 0: #1個目の積み上げ
                new_y -= height
            else:
                new_y -= int(height * 0.1) #どんどんy座標を小さくしていく
        
            screen.blit(info["image"], (base_x, new_y))
        
        
        if judge_result == 1: 
            pg.draw.rect(screen, (70, 255, 240), (470, 100, 210, 60))
            res_text = result_font.render("注文通り！", True, (0, 180, 0)) # 緑色
            screen.blit(res_text, (480, 100))
            next_text = font.render("任意のキーを押して次へ進む", True, (100, 100, 100))
            screen.blit(next_text, (450, 50))

        elif judge_result == 2:
            pg.draw.rect(screen, (255, 140, 80), (450, 100, 250, 60))
            res_text = result_font.render("注文と違う...", True, (200, 0, 0)) # 赤色
            screen.blit(res_text, (460, 100))

            # 0.5秒経過した後にここを通過するため、「任意のキーを押して〜」が表示される
            next_text = font.render("任意のキーを押して次へ進む", True, (100, 100, 100))
            screen.blit(next_text, (450, 50))
        
        pg.display.update()
        clock.tick(60)

    

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()