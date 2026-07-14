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

#スキル2が発動されたときの簡単なメニュー
EASY_RECIPE = {
    1:[3]
}



def get_random_recipe(is_skill2_active = False): #お題となるメニューをランダムに決める

    #スキル２が発動中の場合EASY_RECIPEを用いる
    if (is_skill2_active == False):
        menu_idx = random.choice(list(RECIPES))
    else:
        menu_idx = random.choice(list(EASY_RECIPE))

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


def main():

    #スキル2変数宣言
    is_skill2_active = False
    skill_timer = 0

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

 
    bg_image = load_background_image("haikei_2.jpg", (WIDTH, HEIGHT)) #背景画像の読み込み

    for ing_id, info in zairyo.items(): #材料画像を読み込み
        img, computed_height = load_and_scale_image(info["file_name"], 200)
        if img:
            zairyo[ing_id]["image"] = img
            zairyo[ing_id]["height"] = computed_height 

    #見本のハンバーガー画像読み込み
    menu_img_1 = pg.image.load("image/1_nomal.png")
    menu_img_1 =pg.transform.rotozoom(menu_img_1, 0, 0.08)
    menu_img_2 = pg.image.load("image/2_baconcheese.png")
    menu_img_2 =pg.transform.rotozoom(menu_img_2, 0, 0.08)
    menu_img_3 = pg.image.load("image/3_cheese.png")
    menu_img_3 =pg.transform.rotozoom(menu_img_3, 0, 0.08)
    menu_img_4 = pg.image.load("image/4_beji.png")
    menu_img_4 =pg.transform.rotozoom(menu_img_4, 0, 0.08)
    menu_img_5 = pg.image.load("image/5_double.png")
    menu_img_5 =pg.transform.rotozoom(menu_img_5, 0, 0.08)
    menu_img_6 = pg.image.load("image/6_special.png")
    menu_img_6 =pg.transform.rotozoom(menu_img_6, 0, 0.08)
    menu_img_7 = pg.image.load("image/7_happy.png")
    menu_img_7 =pg.transform.rotozoom(menu_img_7, 0, 0.08)
    bans_img_top = pg.image.load("image/bans_top.png")
    bans_img_top =pg.transform.rotozoom(bans_img_top, 0, 0.08)
    
    # 最初のターゲットレシピをランダムに決定
    target_menu = get_random_recipe(is_skill2_active)

    make_burger = [] #積み上げている材料を保存する
    judge_result = None #判定結果用

    x = True
    
    while x:
        # 背景画像を描画
        if bg_image:
            screen.blit(bg_image, (0, 0))

            #スキル２タイマー
            if is_skill2_active == True:
                skill_timer -= 1
                if skill_timer <= 0:
                    is_skill2_active = False

        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                x = False
                
            elif event.type == pg.KEYDOWN: 
                if judge_result == 1: # クリア時に何かキーを押したら次の注文へ
                    make_burger = []
                    judge_result = None
                    target_menu = get_random_recipe(is_skill2_active)  # 次のレシピをランダム決定
                    continue

                
                if event.key in key_id: # 数字キーに対応して具材を乗せる
                    ing_id = key_id[event.key]
                    make_burger.append(ing_id)
                    judge_result = None 

                elif event.key == pg.K_RETURN:# エンターキーで判定（商品提供）
                    if make_burger == RECIPES[target_menu]:
                        judge_result = 1
                    else:
                        judge_result = 0

                #Eキーを押すかつスコアが30以上でスキル2発動
                if event.key == pg.K_e and score >= 30 and is_skill2_active == False:
                    score -= 30
                    is_skill2_active = True
                    skill_timer = 60*5
                    target_menu = get_random_recipe(is_skill2_active)
                    make_burger = []
                    

                    

                


                
        #ランダムに決定されたtarget_menuに合わせてモニターの位置に見本画像を置く
        if target_menu == 1:
            screen.blit(menu_img_1, (500, 60))
        elif target_menu == 2:
            screen.blit(menu_img_2, (500, 60))
        elif target_menu == 3:
            screen.blit(menu_img_3, (500, 60))
        elif target_menu == 4:
            screen.blit(menu_img_4, (500, 60))
        elif target_menu == 5:
            screen.blit(menu_img_5, (500, 60))
        elif target_menu == 6:
            screen.blit(menu_img_6, (500, 60))
        elif target_menu == 7:
            screen.blit(menu_img_7, (500, 60))


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

        elif judge_result == 0:
            pg.draw.rect(screen, (255, 140, 80), (450, 100, 250, 60))
            res_text = result_font.render("注文と違う...", True, (200, 0, 0)) # 赤色
            screen.blit(res_text, (460, 100))
            gameover = finish_font.render("GAME OVER", True, (200, 0, 0)) # 赤色
            screen.blit(gameover, (400, 325))

            pg.display.update()
            time.sleep(2)
            return 
        
        pg.display.update()
        clock.tick(60)

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()