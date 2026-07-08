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
KEY_MAP = {
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

def load_and_scale_image(file_name, target_width):

    filepath = os.path.join("image", file_name)
    img = pg.image.load(filepath).convert_alpha()
        
    orig_width, orig_height = img.get_size()
    scale_ratio = target_width / orig_width
    new_height = int(orig_height * scale_ratio)
        
    return pg.transform.scale(img, (target_width, new_height)), new_height

def load_background_image(file_name, size):

    filepath = os.path.join("image", file_name)
    img = pg.image.load(filepath).convert_alpha() 
    return pg.transform.scale(img, size)


def main():
    pg.init()
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("ハンバーガー屋を経営しよう")
    clock = pg.time.Clock()
    
    font = pg.font.SysFont("meiryo", 24)
    result_font = pg.font.SysFont("meiryo", 48) 

 
    bg_image = load_background_image("haikei_2.jpg", (WIDTH, HEIGHT)) #背景画像の読み込み

    for ing_id, info in zairyo.items(): #材料画像を読み込み
        img, computed_height = load_and_scale_image(info["file_name"], 200)
        if img:
            zairyo[ing_id]["image"] = img
            zairyo[ing_id]["height"] = computed_height 


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
    target_menu = get_random_recipe()

    make_burger = []
    judge_result = None #判定結果用

    x = True
    while x:
        # 背景画像を描画
        if bg_image:
            screen.blit(bg_image, (0, 0))

        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                x = False
                
            elif event.type == pg.KEYDOWN: # クリア表示が出ている時に何かキーを押したら次の問題へ進む
                if judge_result == 1: 
                    make_burger = []
                    judge_result = None
                    target_menu = get_random_recipe()  # 次のレシピをランダム決定
                    continue

                
                if event.key in KEY_MAP: # 具材を乗せる
                    ing_id = KEY_MAP[event.key]
                    make_burger.append(ing_id)
                    judge_result = None 

                elif event.key == pg.K_SPACE:# スペースキーで判定（商品提供）
                    if make_burger == RECIPES[target_menu]:
                        judge_result = 1
                    else:
                        judge_result = 0

                
                # elif event.key == pg.K_BACKSPACE:#Backspaceを押したら判定表示を消す
                #     if current_burger:
                #         current_burger.pop()
                #     judge_result = None

                
        #ランダムに決定されたtarget_menuに合わせてモニター図位置に見本画像を置く
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
            
            if index == 0:
                new_y -= height
            else:
                new_y -= int(height * 0.1)
        
            screen.blit(info["image"], (base_x, new_y))
        
        # if judge_result is not None:
        #     bans_top_height = bans_img_top.get_height()
        #     # 一番上の具材からさらにバンズの高さ分引いた位置（少し重ねるために+10などの微調整を入れると綺麗です）
        #     bans_y = new_y - bans_top_height + 10 
        #     screen.blit(bans_img_top, (img_x, bans_y))
        
        if judge_result == 1:
            res_text = result_font.render("注文通り！", True, (0, 180, 0)) # 緑色
            screen.blit(res_text, (800, 90))
            next_text = font.render("任意のキーを押して次へ進む", True, (100, 100, 100))
            screen.blit(next_text, (780, 160))
        elif judge_result == 0:
            res_text = result_font.render("注文と違う...", True, (200, 0, 0)) # 赤色
            screen.blit(res_text, (800, 90))
            gameover = result_font.render("GAME OVER", True, (200, 0, 0)) # 赤色
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