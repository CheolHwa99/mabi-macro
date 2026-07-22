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

# 기본 설정 및 전역 변수
pyautogui.FAILSAFE = True 

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

general_run_count = 0
abyss_run_count = 0
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

# f2 일시정지 기능
is_paused = False
pause_key_pressed = False

def check_pause():
    global is_paused, pause_key_pressed
    # F2 키 (0x71) 감지
    current_state = ctypes.windll.user32.GetAsyncKeyState(0x71) & 0x8000
    
    if current_state and not pause_key_pressed:
        pause_key_pressed = True
        is_paused = not is_paused
        if is_paused:
            print("\n일시정지 중입니다.\n")
        else:
            print("\n다시 시작합니다.\n")
    elif not current_state:
        pause_key_pressed = False
        
    # 일시정지 상태면 여기서 무한 대기 (완벽한 멈춤)
    while is_paused:
        current_state = ctypes.windll.user32.GetAsyncKeyState(0x71) & 0x8000
        if current_state and not pause_key_pressed:
            pause_key_pressed = True
            is_paused = False
            print("\n다시 시작합니다.\n")
            break
        elif not current_state:
            pause_key_pressed = False
        time.sleep(0.1)

def smart_sleep(seconds):
    elapsed = 0
    while elapsed < seconds:
        check_pause() # 매 순간 일시정지 체크
        time.sleep(0.05)
        elapsed += 0.05

# 이미지 로딩 및 캡처 함수
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, 'image')

def get_img(filename):
    return os.path.join(IMAGE_DIR, filename)

def get_game_monitor():
    hwnd = win32gui.FindWindow(None, "마비노기 모바일")
    if not hwnd: 
        return None
        
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return {"left": left, "top": top, "width": right - left, "height": bottom - top}

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

# 이미지 변수 모음
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

IMG_CURRENCY_ON = get_img('currency_on.png')       
IMG_CURRENCY_OFF = get_img('currency_off.png')     
IMG_ENTER_BTN = get_img('enter_button.png')        
IMG_GENERAL_ENTER_AGAIN = get_img('general_enter_again.png') 

IMG_ABYSS_TITLE = get_img('abyss_title.png')
IMG_ABYSS_TITLE2 = get_img('abyss_title2.png')
IMG_ABYSS_BANNER1 = get_img('abyss_banner1.png') 
IMG_ABYSS_BANNER2 = get_img('abyss_banner2.png')
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
IMG_ABYSS_ENTER_COOP = get_img('abyss_enter_coop.png')
IMG_ABYSS_RANDOM_ON = get_img('abyss_random_on.png')   
IMG_ABYSS_RANDOM_OFF = get_img('abyss_random_off.png') 
IMG_ABYSS_EXIT_BTN = get_img('abyss_exit_button.png')
IMG_ABYSS_ICON = get_img('abyss_icon.png')

IMG_RAID_TITLE = get_img('raid_title.png')
IMG_RAID_SET_SAIL = get_img('raid_set_sail.png')
IMG_RAID_CONFIRM = get_img('raid_confirm.png')
IMG_RAID_EXIT = get_img('raid_exit.png')
IMG_RAID_MOVE_SHIP = get_img('raid_move_ship.png')

IMG_FISH_STAND = get_img('fish_stand.png')          
IMG_FISH_SIT = get_img('fish_sit.png')              
IMG_FISH_AUTO_MODE = get_img('fish_auto_mode.png')  
IMG_FISH_BITE = get_img('fish_bite.png')            
IMG_FISH_BAD_1 = get_img('fish_bad_1.png')          
IMG_FISH_BAD_2 = get_img('fish_bad_2.png')          

# 공통 편의 함수
def check_coop_popup():
    coop_popup = find_img_center(IMG_COOP_POPUP, 0.8)
    if coop_popup:
        print("협동 미션 팝업 감지.")
        game_click(coop_popup)
        smart_sleep(0.3) 
        return True
    return False

def ask_abyss_options():
    choice = {"dungeon": "dungeon1", "diff": "hard", "party": "coop"}
    root = tk.Tk(); root.title("어비스 자동 진입 설정"); root.geometry("320x330"); root.attributes("-topmost", True)
    
    dungeon_var = tk.StringVar(value="dungeon1")
    diff_var = tk.StringVar(value="hard")
    party_var = tk.StringVar(value="coop")
    
    tk.Label(root, text="◈ 던전 선택 ◈", font=("맑은 고딕", 10, "bold")).pack(pady=5)
    tk.Radiobutton(root, text="허상의 정박지", variable=dungeon_var, value="dungeon1").pack()
    tk.Radiobutton(root, text="광기의 동굴", variable=dungeon_var, value="dungeon2").pack()

    tk.Label(root, text="◈ 난이도 선택 ◈", font=("맑은 고딕", 10, "bold")).pack(pady=5)
    tk.Radiobutton(root, text="쉬움", variable=diff_var, value="easy").pack()
    tk.Radiobutton(root, text="어려움", variable=diff_var, value="hard").pack()
    tk.Radiobutton(root, text="매우 어려움", variable=diff_var, value="very_hard").pack()
    
    tk.Label(root, text="◈ 파티 매칭 선택 ◈", font=("맑은 고딕", 10, "bold")).pack(pady=5)
    tk.Radiobutton(root, text="혼자하기", variable=party_var, value="solo").pack()
    tk.Radiobutton(root, text="함께하기", variable=party_var, value="coop").pack()
    
    def on_confirm():
        choice["dungeon"] = dungeon_var.get()
        choice["diff"] = diff_var.get()
        choice["party"] = party_var.get()
        root.destroy()
        
    tk.Button(root, text="설정 완료 및 시작", width=15, command=on_confirm).pack(pady=10)
    root.mainloop()
    return choice["dungeon"], choice["diff"], choice["party"]

def start_countdown(mode_name):
    print(f"\n{mode_name} 매크로 가동.")
    for i in range(3, 0, -1):
        print(f"{i}초 뒤에 매크로 제어를 시작합니다...")
        time.sleep(1)
    print("제어 상태 진입\n")

# 일반 던전 모듈
def run_general_macro():
    global general_run_count, first_startup_general
    if first_startup_general:
        start_countdown("일반 던전")
        first_startup_general = False
    
    state = "LOBBY" 
    
    while True:
        check_pause() # 시작 전 일시정지 확인
        
        if state == "LOBBY":
            check_coop_popup()
            cont_btn = find_img_center(IMG_CONTINUE_BTN, 0.8)
            if cont_btn: 
                game_click(cont_btn); continue
            
            currency_on = find_img_center(IMG_CURRENCY_ON, 0.8)
            if currency_on: 
                game_click(currency_on); continue
                
            currency_off = find_img_center(IMG_CURRENCY_OFF, 0.8)
            if currency_off:
                random_off = find_img_center(IMG_ABYSS_RANDOM_OFF, 0.8)
                if random_off: game_click(random_off); continue
                
                random_on = find_img_center(IMG_ABYSS_RANDOM_ON, 0.8)
                if random_on:
                    enter_btn = find_img_center(IMG_ENTER_BTN, 0.8)
                    if not enter_btn: enter_btn = find_img_center(IMG_GENERAL_ENTER_AGAIN, 0.8)
                    if enter_btn:
                        game_click(enter_btn)
                        smart_sleep(0.5)
                        week_check = find_img_center(IMG_WEEK_CHECK, 0.8)
                        if week_check: game_click(week_check); smart_sleep(0.1)
                        popup_enter = find_img_center(IMG_POPUP_ENTER, 0.8)
                        if popup_enter: game_click(popup_enter)
                        state = "LOADING"
            smart_sleep(0.2)

        elif state == "LOADING":
            check_coop_popup()
            cont_btn = find_img_center(IMG_CONTINUE_BTN, 0.8)
            if cont_btn: game_click(cont_btn)
            
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn); smart_sleep(0.5)
                while True:
                    check_pause()
                    check_coop_popup(); pyautogui.press('space')
                    if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8): break
                    smart_sleep(0.3)
            
            if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8):
                general_run_count += 1 
                print(f"일반 던전 진행 횟수 (누적: {general_run_count}바퀴 / 가동 시간: {get_uptime()})")
                smart_sleep(0.2); pyautogui.press('space'); smart_sleep(0.1); pyautogui.press('b'); smart_sleep(1.0)
                state = "COMBAT"
            smart_sleep(0.2)

        elif state == "COMBAT":
            check_coop_popup()
            if find_img_center(IMG_CURRENCY_OFF, 0.8) or find_img_center(IMG_CURRENCY_ON, 0.8):
                state = "LOBBY"; continue
                
            if find_img_center(IMG_SKIP_SCENE, 0.8): game_click(find_img_center(IMG_SKIP_SCENE, 0.8)); continue
            if find_img_center(IMG_SEASON_LVLUP, 0.8):
                lvl = find_img_center(IMG_SEASON_LVLUP, 0.8)
                for _ in range(4): game_click_xy(lvl[0], lvl[1]); smart_sleep(0.05)
                continue
            if find_img_center(IMG_AUTO_BTN, 0.8): 
                game_click(find_img_center(IMG_AUTO_BTN, 0.8)); smart_sleep(0.3); pyautogui.press('b'); continue
            if find_img_center(IMG_SKILL_OFF, 0.8): game_click(find_img_center(IMG_SKILL_OFF, 0.8)); continue
            if find_img_center(IMG_BARD_ULT, 0.8): game_click(find_img_center(IMG_BARD_ULT, 0.8)); smart_sleep(0.1); continue

            clear_loc = find_img_center(IMG_CLEAR, 0.8)
            if clear_loc:
                while True:
                    check_pause()
                    check_coop_popup()
                    again_btn = find_img_center(IMG_AGAIN_BTN, 0.8)
                    if again_btn: 
                        game_click(again_btn); smart_sleep(0.5)
                        state = "LOBBY"; break
                    game_click_xy(clear_loc[0], clear_loc[1]); smart_sleep(0.05)
            smart_sleep(0.1)

# 어비스 모듈
def run_abyss_macro():
    global abyss_run_count, first_startup_abyss, cached_abyss_options
    if cached_abyss_options is None: cached_abyss_options = ask_abyss_options()
    
    target_dungeon, target_diff, target_party = cached_abyss_options 
    
    if first_startup_abyss:
        start_countdown(f"어비스 [{target_dungeon} / {target_diff.upper()} / {target_party.upper()}]"); first_startup_abyss = False

    while True:
        # 로비 입장 및 세팅
        while True: 
            check_pause()
            check_coop_popup()
            
            if target_dungeon == "dungeon1":
                banner = find_img_center(IMG_ABYSS_BANNER1, 0.8)
                if banner: game_click(banner)
            else:
                banner = find_img_center(IMG_ABYSS_BANNER2, 0.8)
                if banner: game_click(banner)
            
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

            # 입장 클릭 (솔로/파티 통일됨)
            if target_party == "coop":
                btn_r_off = find_img_center(IMG_ABYSS_RANDOM_OFF, 0.8)
                if btn_r_off: game_click(btn_r_off); smart_sleep(0.1)
                
            abyss_enter = find_img_center(IMG_ABYSS_ENTER_COOP, 0.8)
            if abyss_enter: game_click(abyss_enter); break 
            smart_sleep(0.1)

        # 로딩
        while True: 
            check_pause()
            check_coop_popup()
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn); smart_sleep(0.5)
                while True:
                    check_pause()
                    check_coop_popup(); pyautogui.press('space')
                    if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8): break
                    smart_sleep(0.3)
            
            if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8):
                abyss_run_count += 1 
                print(f"어비스 진행 횟수 (누적: {abyss_run_count}바퀴 / 가동 시간: {get_uptime()})")
                smart_sleep(0.1); pyautogui.press('space'); smart_sleep(0.1); pyautogui.press('b'); smart_sleep(1.0); break
            smart_sleep(0.2)

        # 전투
        while True: 
            check_pause()
            check_coop_popup()
            if find_img_center(IMG_SKIP_SCENE, 0.8): game_click(find_img_center(IMG_SKIP_SCENE, 0.8)); continue
            if find_img_center(IMG_SEASON_LVLUP, 0.8):
                lvl = find_img_center(IMG_SEASON_LVLUP, 0.8)
                for _ in range(4): game_click_xy(lvl[0], lvl[1]); smart_sleep(0.05)
                continue
            if find_img_center(IMG_AUTO_BTN, 0.8): 
                game_click(find_img_center(IMG_AUTO_BTN, 0.8)); smart_sleep(0.3); pyautogui.press('b'); continue
            if find_img_center(IMG_SKILL_OFF, 0.8): game_click(find_img_center(IMG_SKILL_OFF, 0.8)); continue
            if find_img_center(IMG_BARD_ULT, 0.8): game_click(find_img_center(IMG_BARD_ULT, 0.8)); smart_sleep(0.1); continue

            clear_loc = find_img_center(IMG_CLEAR, 0.8)
            if clear_loc:
                while True:
                    check_pause()
                    check_coop_popup()
                    abyss_exit_btn = find_img_center(IMG_ABYSS_EXIT_BTN, 0.8)
                    if abyss_exit_btn: game_click(abyss_exit_btn); break
                    game_click_xy(clear_loc[0], clear_loc[1]); smart_sleep(0.05)
                break 
            smart_sleep(0.1)

        # 마을 복귀 및 재입장
        while True:
            check_pause()
            if check_coop_popup(): continue 
            
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn:
                game_click(retry_btn); smart_sleep(0.5)
                while True:
                    check_pause()
                    if check_coop_popup(): continue
                    pyautogui.press('space')
                    if find_img_center(IMG_MENU_BTN, 0.8): game_click(find_img_center(IMG_MENU_BTN, 0.8)); smart_sleep(0.5); break
                    smart_sleep(0.3)
                continue

            if target_dungeon == "dungeon1":
                banner = find_img_center(IMG_ABYSS_BANNER1, 0.8)
                if banner: game_click(banner); smart_sleep(0.5); break 
            else:
                banner = find_img_center(IMG_ABYSS_BANNER2, 0.8)
                if banner: game_click(banner); smart_sleep(0.5); break 

            abyss_icon = find_img_center(IMG_ABYSS_ICON, 0.8)
            if abyss_icon: game_click(abyss_icon); smart_sleep(0.5); continue 

            menu_btn = find_img_center(IMG_MENU_BTN, 0.8)
            if menu_btn: game_click(menu_btn); smart_sleep(0.5); continue
            smart_sleep(0.1)

# 매크로 모듈
def run_raid_macro():
    global raid_run_count, first_startup_raid
    if first_startup_raid:
        start_countdown("레이드") 
        first_startup_raid = False

    state = "LOBBY" 
    
    while True:
        check_pause()
        
        if state == "LOBBY":
            check_coop_popup()
            solo_off = find_img_center(IMG_ABYSS_SOLO_OFF, 0.8)
            if solo_off: game_click(solo_off); smart_sleep(0.3); continue
                
            set_sail = find_img_center(IMG_RAID_SET_SAIL, 0.8)
            if set_sail:
                game_click(set_sail)
                print("배로 출항합니다. 로딩 대기 중...")
                smart_sleep(1.0)
                state = "SHIP"
            smart_sleep(0.2)

        elif state == "SHIP":
            check_coop_popup()
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn: game_click(retry_btn); smart_sleep(0.5); continue
            
            auto_btn = find_img_center(IMG_AUTO_BTN, 0.8)
            if auto_btn:
                game_click(auto_btn)
                smart_sleep(1.0)
                state = "ENTERING_BOSS"
            smart_sleep(0.2)

        elif state == "ENTERING_BOSS":
            check_coop_popup()
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn: game_click(retry_btn); smart_sleep(0.5); continue
                
            skip_scene = find_img_center(IMG_SKIP_SCENE, 0.8)
            if skip_scene:
                game_click(skip_scene)
                smart_sleep(0.5)
                continue
                
            if find_img_center(IMG_SKILL_OFF, 0.8) or find_img_center(IMG_SKILL_ON, 0.8):
                raid_run_count += 1
                print(f"레이드 진행 횟수 (누적: {raid_run_count}바퀴 / 가동 시간: {get_uptime()})")
                smart_sleep(0.1); pyautogui.press('space'); smart_sleep(0.1); pyautogui.press('b'); smart_sleep(1.0)
                state = "COMBAT"
            smart_sleep(0.1) 

        elif state == "COMBAT":
            check_coop_popup()
            if find_img_center(IMG_SKIP_SCENE, 0.8): game_click(find_img_center(IMG_SKIP_SCENE, 0.8)); continue
            if find_img_center(IMG_SEASON_LVLUP, 0.8):
                lvl = find_img_center(IMG_SEASON_LVLUP, 0.8)
                for _ in range(4): game_click_xy(lvl[0], lvl[1]); smart_sleep(0.05)
                continue
            if find_img_center(IMG_AUTO_BTN, 0.8): 
                game_click(find_img_center(IMG_AUTO_BTN, 0.8)); smart_sleep(0.3); pyautogui.press('b'); continue
            if find_img_center(IMG_SKILL_OFF, 0.8): game_click(find_img_center(IMG_SKILL_OFF, 0.8)); continue
            if find_img_center(IMG_BARD_ULT, 0.8): game_click(find_img_center(IMG_BARD_ULT, 0.8)); smart_sleep(0.1); continue

            raid_confirm = find_img_center(IMG_RAID_CONFIRM, 0.8)
            if raid_confirm:
                game_click(raid_confirm)
                smart_sleep(1.0)
                state = "ENDING"
            smart_sleep(0.1)
            
        elif state == "ENDING":
            check_coop_popup()
            retry_btn = find_img_center(IMG_RETRY_BTN, 0.8)
            if retry_btn: game_click(retry_btn); smart_sleep(0.5); continue
            
            raid_exit = find_img_center(IMG_RAID_EXIT, 0.8)
            if raid_exit: game_click(raid_exit); smart_sleep(0.5); continue
                
            move_ship = find_img_center(IMG_RAID_MOVE_SHIP, 0.8)
            if move_ship:
                game_click(move_ship)
                smart_sleep(1.5)
                state = "SHIP"
            smart_sleep(0.2)

# 낚시 모듈
def run_fishing_macro():
    global fish_run_count, first_startup_fish
    if first_startup_fish:
        start_countdown("수동 필터링 낚시") 
        first_startup_fish = False

    while True:
        check_pause()
        check_coop_popup()
        start_btn = find_img_center(IMG_FISH_STAND, 0.8)
        if not start_btn: start_btn = find_img_center(IMG_FISH_SIT, 0.8)
            
        if start_btn:
            game_click(start_btn)
            smart_sleep(1.0) 

        check_coop_popup()
        auto_icon = find_img_center(IMG_FISH_AUTO_MODE, 0.8)
        if auto_icon:
            game_click(auto_icon)
            smart_sleep(0.2)
            pyautogui.press('space')
            smart_sleep(0.5)

        bite_loc = None
        fishing_canceled = False
        while True:
            check_pause()
            check_coop_popup()
            cancel_btn = find_img_center(IMG_FISH_STAND, 0.8)
            if not cancel_btn: cancel_btn = find_img_center(IMG_FISH_SIT, 0.8)
                
            if cancel_btn:
                game_click(cancel_btn)
                smart_sleep(1.0)
                fishing_canceled = True
                break
            
            bite_loc = find_img_center(IMG_FISH_BITE, 0.8)
            if bite_loc: break
            smart_sleep(0.1)

        if fishing_canceled: continue 

        check_coop_popup()
        
        bad_text_found = False
        for _ in range(10):
            if find_img_center(IMG_FISH_BAD_1, 0.8) or find_img_center(IMG_FISH_BAD_2, 0.8):
                bad_text_found = True
                break
            smart_sleep(0.05)

        if bad_text_found:
            print("쓰레기 감지 취소합니다.")
            pyautogui.keyDown('w'); smart_sleep(0.1); pyautogui.keyUp('w') # 단순 press보다 빠르고 확실한 캔슬법
            smart_sleep(1.5)
            continue
            
        # 쓰레기가 아니면 나머지 낚시 시간 대기
        smart_sleep(5.0)
        
        final_bite = find_img_center(IMG_FISH_BITE, 0.8)
        if final_bite: game_click(final_bite)
        else: game_click(bite_loc)
            
        fish_run_count += 1
        print(f"낚시 횟수 (누적: {fish_run_count}회 / 가동 시간: {get_uptime()})\n")
        smart_sleep(0.2)

# ======================================================================
# 🏁 9. 메인 구동 모듈
# ======================================================================
def main():
    print("========================================")
    print("마비노기 모바일 매크로 가동 준비 완료")
    print("작동 중 'F2' 키를 누르면 일시정지됩니다.")
    print("========================================\n")
    
    try:
        while True:
            check_pause() # 메인 화면에서도 일시정지 체크
            check_coop_popup()
            
            general_trigger = find_img_center(IMG_CURRENCY_ON, 0.8)
            if not general_trigger: general_trigger = find_img_center(IMG_CURRENCY_OFF, 0.8)
            if general_trigger:
                run_general_macro()
                continue
                
            abyss_trigger = find_img_center(IMG_ABYSS_TITLE, 0.8)
            if not abyss_trigger: abyss_trigger = find_img_center(IMG_ABYSS_TITLE2, 0.8)
            if abyss_trigger:
                run_abyss_macro()
                continue
                
            raid_trigger = find_img_center(IMG_RAID_TITLE, 0.8)
            if raid_trigger:
                run_raid_macro()
                continue
            
            fish_trigger = find_img_center(IMG_FISH_STAND, 0.8)
            if not fish_trigger: fish_trigger = find_img_center(IMG_FISH_SIT, 0.8)
            if fish_trigger:
                run_fishing_macro()
                continue

            smart_sleep(0.2) 

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
