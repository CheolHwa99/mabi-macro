import pyautogui
import time
import sys
import os
import ctypes 
import cv2
import numpy as np
import tkinter as tk
import win32gui
import win32con
from mss import MSS

# 안전 장치 설정
pyautogui.FAILSAFE = True 

# 윈도우 (DPI) 오차 해결
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# 전역 변수 설정 (횟수 카운터)
fish_run_count = 0
raid_run_count = 0
first_startup_general = True
first_startup_abyss = True
first_startup_raid = True
first_startup_fish = True
cached_abyss_options = None
sct = MSS()
MACRO_START_TIME = time.time()

def get_uptime():
    sec = int(time.time() - MACRO_START_TIME)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    if h > 0: return f"{h}시간 {m}분 {s}초"
    elif m > 0: return f"{m}분 {s}초"
    else: return f"{s}초"


# 한글 경로 안전 이미지 로더
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, 'image')

def get_img(filename):
    return os.path.join(IMAGE_DIR, filename)

# 마비노기 모바일 창 영역 캡처
def get_game_monitor():
    hwnd = win32gui.FindWindow(None, "마비노기 모바일")
    if not hwnd: 
        return None
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return {"left": left, "top": top, "width": right - left, "height": bottom - top}

# 창 내부 전용 이미지 스캔
def find_img_center(img_path, conf=0.8): 
    monitor = get_game_monitor()
    if not monitor: return None
    try:
        screenshot = sct.grab(monitor)
        screen_img = np.array(screenshot)
        screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGRA2GRAY) 
        img_array = np.fromfile(img_path, np.uint8)
        template = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
        if template is None: return None
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= conf:
            h, w = template.shape[:2]
            center_x = max_loc[0] + (w // 2) + monitor['left']
            center_y = max_loc[1] + (h // 2) + monitor['top']
            return (center_x, center_y)
        return None
    except Exception as e: 
        print(f"이미지 스캔 오류: {e}")
        return None

def game_click(target):
    if target:
        x, y = target
        pyautogui.moveTo(x, y) 
        pyautogui.mouseDown()                
        time.sleep(0.05)                      
        pyautogui.mouseUp()
        pyautogui.moveTo(10, 10) 
        
def game_click_xy(x, y):
    pyautogui.moveTo(x, y) 
    pyautogui.mouseDown()
    time.sleep(0.05)
    pyautogui.mouseUp()

# --- 이미지 파일 변수 ---
IMG_RETRY_BTN = get_img('retry_button.png')        
IMG_CONTINUE_BTN = get_img('continue_button.png')  
IMG_POPUP_ENTER = get_img('popup_enter_button.png') 
IMG_WEEK_CHECK = get_img('do_not_show_week.png')   
IMG_SKIP_SCENE = get_img('skip_scene.png')         
IMG_CLEAR = get_img('dungeon_clear.png')           
IMG_AGAIN_BTN = get_img('again_button.png')        
IMG_SEASON_LVLUP = get_img('season_levelup.png')   
IMG_AUTO_BTN = get_img('auto_play_button.png')     
IMG_SKILL_OFF = get_img('skill_auto_off.png')      
IMG_SKILL_ON = get_img('skill_auto_on.png')        
IMG_BARD_ULT = get_img('bard_ult_button.png')
IMG_MENU_BTN = get_img('menu_button.png')          
IMG_COOP_POPUP = get_img('coop_popup.png')

# 던전용 변수
IMG_CURRENCY_ON = get_img('currency_on.png')       
IMG_CURRENCY_OFF = get_img('currency_off.png')     
IMG_ENTER_BTN = get_img('enter_button.png')        
IMG_GENERAL_ENTER_AGAIN = get_img('general_enter_again.png') 
IMG_ABYSS_TITLE = get_img('abyss_title.png')
IMG_ABYSS_TITLE2 = get_img('abyss_title2.png')
IMG_ABYSS_EASY_ON = get_img('abyss_easy_on.png')
IMG_ABYSS_EASY_OFF = get_img('abyss_easy_off.png')
IMG_ABYSS_HARD_ON = get_img('abyss_hard_on.png')
IMG_ABYSS_HARD_OFF = get_img('abyss_hard_off.png')
IMG_ABYSS_VERY_HARD_ON = get_img('abyss_very_hard_on.png')
IMG_ABYSS_VERY_HARD_OFF = get_img('abyss_very_hard_off.png')
IMG_ABYSS_SOLO_ON = get_img('abyss_solo_on.png')
IMG_ABYSS_SOLO_OFF = get_img('abyss_solo_off.png')
IMG_ABYSS_COOP_ON = get_img('abyss_coop_on.png')
IMG_ABYSS_COOP_OFF = get_img('abyss_coop_off.png')
IMG_ABYSS_ENTER_SOLO = get_img('abyss_enter_solo.png')
IMG_ABYSS_ENTER_COOP = get_img('abyss_enter_coop.png')
IMG_ABYSS_RANDOM_ON = get_img('abyss_random_on.png')   
IMG_ABYSS_RANDOM_OFF = get_img('abyss_random_off.png') 
IMG_ABYSS_EXIT_BTN = get_img('abyss_exit_button.png')
IMG_ABYSS_ICON = get_img('abyss_icon.png')
IMG_ABYSS_MENU_SELECT = get_img('abyss_menu_select.png')

# 레이드용 변수 🌟
IMG_RAID_TITLE = get_img('raid_title.png')
IMG_RAID_SET_SAIL = get_img('raid_set_sail.png')
IMG_RAID_CONFIRM = get_img('raid_confirm.png')
IMG_RAID_EXIT = get_img('raid_exit.png')
IMG_RAID_MOVE_SHIP = get_img('raid_move_ship.png')

# 낚시용 변수
IMG_FISH_STAND = get_img('fish_stand.png')          
IMG_FISH_SIT = get_img('fish_sit.png')              
IMG_FISH_AUTO_MODE = get_img('fish_auto_mode.png')  
IMG_FISH_BITE = get_img('fish_bite.png')            
IMG_FISH_BAD_1 = get_img('fish_bad_1.png')          
IMG_FISH_BAD_2 = get_img('fish_bad_2.png')          

# 상시 팝업 처리
def check_coop_popup():
    coop_popup = find_img_center(IMG_COOP_POPUP, 0.8)
    if coop_popup:
        print("협동 미션 팝업 감지.")
        game_click(coop_popup)
        time.sleep(0.3) 
        return True
    return False

def ask_abyss_options():
    choice = {"diff": "hard", "party": "coop"}
    root = tk.Tk(); root.title("어비스 자동 진입 설정"); root.geometry("320x240"); root.attributes("-topmost", True)
    diff_var = tk.StringVar(value="hard"); party_var = tk.StringVar(value="coop")
    tk.Label(root, text="◈ 난이도 선택 ◈", font=("맑은 고딕", 10, "bold")).pack(pady=5)
    tk.Radiobutton(root, text="쉬움", variable=diff_var, value="easy").pack()
    tk.Radiobutton(root, text="어려움", variable=diff_var, value="hard").pack()
    tk.Radiobutton(root, text="매우 어려움", variable=diff_var, value="very_hard").pack()
    tk.Label(root, text="◈ 파티 매칭 선택 ◈", font=("맑은 고딕", 10, "bold")).pack(pady=5)
    tk.Radiobutton(root, text="혼자하기", variable=party_var, value="solo").pack()
    tk.Radiobutton(root, text="함께하기", variable=party_var, value="coop").pack()
    def on_confirm():
        choice["diff"] = diff_var.get(); choice["party"] = party_var.get(); root.destroy()
    tk.Button(root, text="설정 완료 및 시작", width=15, command=on_confirm).pack(pady=10)
    root.mainloop()
    return choice["diff"], choice["party"]

def start_countdown(mode_name):
    print(f"\n{mode_name} 매크로 가동.")
    for i in range(3, 0, -1):
        print(f"{i}초 뒤에 매크로 제어를 시작합니다...")
        time.sleep(1)
    print("제어 상태 진입\n")


#  일반 던전 전용 상태 머신
def run_general_macro():
    global general_run_count, first_startup_general
    if first_startup_general:
        start_countdown("일반 던전")
        first_startup_general = False
    
    state = "LOBBY" 
    
    while True:
        # 로비 세팅 및 입장
        if state == "LOBBY":
            check_coop_popup()

            # 못끝낸 임무 확인
            cont_btn = find_img_center(IMG_CONTINUE_BTN, 0.8)
            if cont_btn: 
                game_click(cont_btn)
                continue
            
            # 재화 체크
            currency_on = find_img_center(IMG_CURRENCY_ON, 0.8)
            if currency_on: 
                game_click(currency_on)
                continue
                
            # 재화 확인후 우연한 만남 확인
            currency_off = find_img_center(IMG_CURRENCY_OFF, 0.8)
            if currency_off:
                random_off = find_img_center(IMG_ABYSS_RANDOM_OFF, 0.8)
                if random_off:
                    game_click(random_off)
                    continue
                random_on = find_img_center(IMG_ABYSS_RANDOM_ON, 0.8)
                if random_on:
                    # 던전 입장버튼 2개 확인
                    enter_btn = find_img_center(IMG_ENTER_BTN, 0.8)
                    if not enter_btn:
                        enter_btn = find_img_center(IMG_GENERAL_ENTER_AGAIN, 0.8)

                    if enter_btn:
                        game_click(enter_btn)
                        time.sleep(0.5)
                        
                        # 팝업 체크
                        week_check = find_img_center(IMG_WEEK_CHECK, 0.8)
                        if week_check:
                            game_click(week_check)
                            time.sleep(0.1)
                            
                        popup_enter = find_img_center(IMG_POPUP_ENTER, 0.8)
                        if popup_enter:
                            game_click(popup_enter)
                        
                        state = "LOADING"
            time.sleep(0.2)

        # 던전 로딩 대기
        elif state == "LOADING":
            check_coop_popup()
            
            # 입장 중 뜰 수 있는 미완료 경고창 스킵
            cont_btn = find_img_center(IMG_CONTINUE_BTN, 0.8)
            if cont_btn: game_click(cont_btn)
            
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn); time.sleep(0.5)
                while True:
                    check_coop_popup(); pyautogui.press('space')
                    if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8): break
                    time.sleep(0.3)
            
            if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8):
                general_run_count += 1 
                print(f"던전 진행 횟수 (누적: {general_run_count}바퀴 / 가동 시간: {get_uptime()})")
                time.sleep(0.2); pyautogui.press('space'); time.sleep(0.1); pyautogui.press('b'); time.sleep(1.0)
                state = "COMBAT"
            time.sleep(0.2)

        # 던전 전투 감시
        elif state == "COMBAT":
            check_coop_popup()
            
            # 혹시라도 로비로 튕겼을 경우를 대비한 방어 코드
            if find_img_center(IMG_CURRENCY_OFF, 0.8) or find_img_center(IMG_CURRENCY_ON, 0.8):
                state = "LOBBY"
                continue
                
            if find_img_center(IMG_SKIP_SCENE, 0.8): game_click(find_img_center(IMG_SKIP_SCENE, 0.8)); continue
            if find_img_center(IMG_SEASON_LVLUP, 0.8):
                lvl = find_img_center(IMG_SEASON_LVLUP, 0.8)
                for _ in range(4): game_click_xy(lvl[0], lvl[1]); time.sleep(0.05)
                continue
            if find_img_center(IMG_AUTO_BTN, 0.8): 
                game_click(find_img_center(IMG_AUTO_BTN, 0.8)); time.sleep(0.3); pyautogui.press('b'); continue
            if find_img_center(IMG_SKILL_OFF, 0.8): game_click(find_img_center(IMG_SKILL_OFF, 0.8)); continue
            if find_img_center(IMG_BARD_ULT, 0.8): game_click(find_img_center(IMG_BARD_ULT, 0.8)); time.sleep(0.1); continue

            clear_loc = find_img_center(IMG_CLEAR, 0.8)
            if clear_loc:
                while True:
                    check_coop_popup()
                    again_btn = find_img_center(IMG_AGAIN_BTN, 0.8)
                    if again_btn: 
                        game_click(again_btn)
                        time.sleep(0.5)
                        state = "LOBBY"
                        break
                    game_click_xy(clear_loc[0], clear_loc[1]); time.sleep(0.05)
            time.sleep(0.1)


# 어비스 전용 상태 머신
def run_abyss_macro():
    global abyss_run_count, first_startup_abyss, cached_abyss_options
    if cached_abyss_options is None: cached_abyss_options = ask_abyss_options()
    target_diff, target_party = cached_abyss_options
    
    if first_startup_abyss:
        start_countdown(f"어비스 던전 [{target_diff.upper()} / {target_party.upper()}]"); first_startup_abyss = False

    while True:
        while True: 
            check_coop_popup()
            if target_diff == "easy":
                btn_off = find_img_center(IMG_ABYSS_EASY_OFF, 0.8)
                if btn_off: game_click(btn_off)
            elif target_diff == "hard": 
                btn_off = find_img_center(IMG_ABYSS_HARD_OFF, 0.8)
                if btn_off: game_click(btn_off)
            elif target_diff == "very_hard":
                btn_off = find_img_center(IMG_ABYSS_VERY_HARD_OFF, 0.8)
                if btn_off: game_click(btn_off)
                    
            if target_party == "solo":
                btn_off = find_img_center(IMG_ABYSS_SOLO_OFF, 0.8)
                if btn_off: game_click(btn_off)
            else: 
                btn_off = find_img_center(IMG_ABYSS_COOP_OFF, 0.8)
                if btn_off: game_click(btn_off)

            if target_party == "solo":
                abyss_enter = find_img_center(IMG_ABYSS_ENTER_SOLO, 0.8)
                if abyss_enter: game_click(abyss_enter); break 
            else:
                btn_r_off = find_img_center(IMG_ABYSS_RANDOM_OFF, 0.8)
                if btn_r_off: 
                    game_click(btn_r_off); time.sleep(0.1)
                    
                abyss_enter = find_img_center(IMG_ABYSS_ENTER_COOP, 0.8)
                if abyss_enter: game_click(abyss_enter); break 
            time.sleep(0.1)

        while True: 
            check_coop_popup()
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn); time.sleep(0.5)
                while True:
                    check_coop_popup(); pyautogui.press('space')
                    if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8): break
                    time.sleep(0.3)
            
            if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8):
                abyss_run_count += 1 
                print(f"어비스 진행 횟수 (누적: {abyss_run_count}바퀴 / 가동 시간: {get_uptime()})")
                time.sleep(0.1); pyautogui.press('space'); time.sleep(0.1); pyautogui.press('b'); time.sleep(1.0); break
            time.sleep(0.2)

        while True: 
            check_coop_popup()
            if find_img_center(IMG_SKIP_SCENE, 0.8): game_click(find_img_center(IMG_SKIP_SCENE, 0.8)); continue
            if find_img_center(IMG_SEASON_LVLUP, 0.8):
                lvl = find_img_center(IMG_SEASON_LVLUP, 0.8)
                for _ in range(4): game_click_xy(lvl[0], lvl[1]); time.sleep(0.05)
                continue
            if find_img_center(IMG_AUTO_BTN, 0.8): 
                game_click(find_img_center(IMG_AUTO_BTN, 0.8)); time.sleep(0.3); pyautogui.press('b'); continue
            if find_img_center(IMG_SKILL_OFF, 0.8): game_click(find_img_center(IMG_SKILL_OFF, 0.8)); continue
            if find_img_center(IMG_BARD_ULT, 0.8): game_click(find_img_center(IMG_BARD_ULT, 0.8)); time.sleep(0.1); continue

            clear_loc = find_img_center(IMG_CLEAR, 0.8)
            if clear_loc:
                while True:
                    check_coop_popup()
                    abyss_exit_btn = find_img_center(IMG_ABYSS_EXIT_BTN, 0.8)
                    if abyss_exit_btn: game_click(abyss_exit_btn); break
                    game_click_xy(clear_loc[0], clear_loc[1]); time.sleep(0.05)
                break 
            time.sleep(0.1)

        print("마을 복귀 및 재입장 감시 중...")
        while True:
            if check_coop_popup(): continue 
            
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn); time.sleep(0.5)
                while True:
                    if check_coop_popup(): continue
                    pyautogui.press('space')
                    if find_img_center(IMG_MENU_BTN, 0.8): game_click(find_img_center(IMG_MENU_BTN, 0.8)); time.sleep(0.5); break
                    time.sleep(0.3)
                continue

            abyss_menu = find_img_center(IMG_ABYSS_MENU_SELECT, 0.8)
            if abyss_menu: game_click(abyss_menu); time.sleep(0.5); break 

            abyss_icon = find_img_center(IMG_ABYSS_ICON, 0.8)
            if abyss_icon: game_click(abyss_icon); time.sleep(0.5); continue 

            menu_btn = find_img_center(IMG_MENU_BTN, 0.8)
            if menu_btn: game_click(menu_btn); time.sleep(0.5); continue
            time.sleep(0.1)

# 레이드 전용 상태 머신
def run_raid_macro():
    global raid_run_count, first_startup_raid
    
    if first_startup_raid:
        start_countdown("레이드") 
        first_startup_raid = False

    state = "LOBBY" 
    
    while True:
        # 로비에서 혼자하기 세팅 및 출항
        if state == "LOBBY":
            check_coop_popup()
            
            solo_off = find_img_center(IMG_ABYSS_SOLO_OFF, 0.8)
            if solo_off:
                game_click(solo_off)
                time.sleep(0.3)
                continue
                
            set_sail = find_img_center(IMG_RAID_SET_SAIL, 0.8)
            if set_sail:
                game_click(set_sail)
                print("배로 출항합니다! 로딩 대기 중...")
                time.sleep(1.0)
                state = "SHIP"
            time.sleep(0.2)

        # 배 안
        elif state == "SHIP":
            check_coop_popup()
            
            # 서버 끊김 방어
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn)
                time.sleep(0.5)
                continue
            
            # 배 안으로 돌아와서 자동 진행 버튼이 보이면 전투 진입 시도
            auto_btn = find_img_center(IMG_AUTO_BTN, 0.8)
            if auto_btn:
                game_click(auto_btn)
                print("자동 진행 클릭! 보스방으로 들어갑니다.")
                time.sleep(1.0)
                state = "ENTERING_BOSS"
            time.sleep(0.2)

        # 레이드 진입
        elif state == "ENTERING_BOSS":
            check_coop_popup()
            
            # 서버 끊김 방어
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn)
                time.sleep(0.5)
                continue
                
            # 스킵 버튼 감시
            skip_scene = find_img_center(IMG_SKIP_SCENE, 0.8)
            if skip_scene:
                game_click(skip_scene)
                print("컷신 스킵 버튼 클릭!")
                time.sleep(0.5)
                continue
                
            # 스킬 UI가 보이면 컷신이 끝났거나 전투가 시작된 것
            if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8):
                raid_run_count += 1
                print(f"🐉 레이드 보스 진입 완료! (누적: {raid_run_count}바퀴 / 가동 시간: {get_uptime()})")
                time.sleep(0.1); pyautogui.press('space'); time.sleep(0.1); pyautogui.press('b'); time.sleep(1.0)
                state = "COMBAT"
            time.sleep(0.1) # 감시 주기를 매우 짧게!

        # 전투 진행 및 클리어 확인
        elif state == "COMBAT":
            check_coop_popup()
            
            if find_img_center(IMG_SKIP_SCENE, 0.8): game_click(find_img_center(IMG_SKIP_SCENE, 0.8)); continue
            if find_img_center(IMG_SEASON_LVLUP, 0.8):
                lvl = find_img_center(IMG_SEASON_LVLUP, 0.8)
                for _ in range(4): game_click_xy(lvl[0], lvl[1]); time.sleep(0.05)
                continue
            if find_img_center(IMG_AUTO_BTN, 0.8): 
                game_click(find_img_center(IMG_AUTO_BTN, 0.8)); time.sleep(0.3); pyautogui.press('b'); continue
            if find_img_center(IMG_SKILL_OFF, 0.8): game_click(find_img_center(IMG_SKILL_OFF, 0.8)); continue
            if find_img_center(IMG_BARD_ULT, 0.8): game_click(find_img_center(IMG_BARD_ULT, 0.8)); time.sleep(0.1); continue

            # 전투 종료 레이드 확인 버튼 감시
            raid_confirm = find_img_center(IMG_RAID_CONFIRM, 0.8)
            if raid_confirm:
                game_click(raid_confirm)
                time.sleep(1.0)
                state = "ENDING"
            time.sleep(0.1)
            
        # 퇴장 및 출항선으로 이동
        elif state == "ENDING":
            check_coop_popup()
            
            # 나가기 로딩 중 튕김 방어
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn)
                time.sleep(0.5)
                continue
            
            # 레이드 나가기 버튼
            raid_exit = find_img_center(IMG_RAID_EXIT, 0.8)
            if raid_exit:
                game_click(raid_exit)
                time.sleep(0.5)
                continue
                
            # 출항선으로 이동 버튼
            move_ship = find_img_center(IMG_RAID_MOVE_SHIP, 0.8)
            if move_ship:
                game_click(move_ship)
                print("배로 복귀합니다.")
                time.sleep(1.5)
                state = "SHIP"
            time.sleep(0.2)

# 낚시 전용 상태 머신
def run_fishing_macro():
    global fish_run_count, first_startup_fish
    
    if first_startup_fish:
        start_countdown("수동 필터링 낚시") 
        first_startup_fish = False

    while True:
        check_coop_popup()
        print(" 준비 상태 파악 및 시작..")
        
        start_btn = find_img_center(IMG_FISH_STAND, 0.8)
        if not start_btn: start_btn = find_img_center(IMG_FISH_SIT, 0.8)
            
        if start_btn:
            game_click(start_btn)
            time.sleep(1.0) 

        check_coop_popup()
        auto_icon = find_img_center(IMG_FISH_AUTO_MODE, 0.8)
        if auto_icon:
            print("수동 낚시로 전환합니다.")
            game_click(auto_icon)
            time.sleep(0.2)
            pyautogui.press('space')
            time.sleep(0.5)

        print("물고기를 기다리는 중...")
        bite_loc = None
        fishing_canceled = False
        while True:
            check_coop_popup()
            
            cancel_btn = find_img_center(IMG_FISH_STAND, 0.8)
            if not cancel_btn: cancel_btn = find_img_center(IMG_FISH_SIT, 0.8)
                
            if cancel_btn:
                game_click(cancel_btn)
                time.sleep(1.0)
                fishing_canceled = True
                break
            
            bite_loc = find_img_center(IMG_FISH_BITE, 0.8)
            if bite_loc:
                print("물고기가 물었습니다.")
                break
                
            time.sleep(0.1)

        if fishing_canceled:
            continue 

        time.sleep(0.5) 
        check_coop_popup()
        
        bad_text_found = False
        if find_img_center(IMG_FISH_BAD_1, 0.8) or find_img_center(IMG_FISH_BAD_2, 0.8):
            bad_text_found = True

        if bad_text_found:
            print("쓰레기 감지. 취소후 재시작 합니다.")
            pyautogui.press('w')
            time.sleep(1.5)
            continue
            
        time.sleep(5.5)
        
        final_bite = find_img_center(IMG_FISH_BITE, 0.8)
        if final_bite:
            game_click(final_bite)
        else:
            game_click(bite_loc)
            
        fish_run_count += 1
        print(f"낚시 횟수 (누적: {fish_run_count}회 / 가동 시간: {get_uptime()})\n")
        time.sleep(0.2)


# 최초 메인 스캔 루프
def main():
    print("========================================")
    print("마비노기 모바일 매크로 가동 완료")
    print("========================================\n")
    
    try:
        while True:
            check_coop_popup()
            
            # 재화 ON/OFF 둘 중 하나만 보여도 일반 던전으로 인식하도록 보완
            general_trigger = find_img_center(IMG_CURRENCY_ON, 0.8)
            if not general_trigger: 
                general_trigger = find_img_center(IMG_CURRENCY_OFF, 0.8)
                
            if general_trigger:
                run_general_macro()
                continue
                
            abyss_trigger = find_img_center(IMG_ABYSS_TITLE, 0.8)
            if not abyss_trigger:
                abyss_trigger = find_img_center(IMG_ABYSS_TITLE2, 0.8)

            if abyss_trigger:
                run_abyss_macro()
                continue
                
            raid_trigger = find_img_center(IMG_RAID_TITLE, 0.8)
            if raid_trigger:
                run_raid_macro()
                continue
            
            fish_trigger = find_img_center(IMG_FISH_STAND, 0.8)
            if not fish_trigger:
                fish_trigger = find_img_center(IMG_FISH_SIT, 0.8)
            if fish_trigger:
                run_fishing_macro()
                continue

            time.sleep(0.2) 

    except pyautogui.FailSafeException:
        print("\n마우스가 모서리로 이동하여 매크로를 강제 종료합니다.")
    except KeyboardInterrupt:
        print("\n사용자가 매크로를 수동으로 중지했습니다. (Ctrl+C)")

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if __name__ == "__main__":
    if is_admin():
        main()
    else:
        print("관리자 권한 승인이 필요합니다. 팝업창에서 '예'를 눌러주세요...")
        if getattr(sys, 'frozen', False):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
