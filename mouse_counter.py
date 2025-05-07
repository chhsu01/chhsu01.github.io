import time
import threading
from pynput import mouse
import win32gui
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = 'mouse_clicks_log.csv'

# 支援的應用程式關鍵字
TARGET_APPS = ['AutoCAD', 'Revit']

# 點擊計數（分別記錄 AutoCAD 與 Revit 的 left/right/middle）
def load_last_counts():
    counts = {
        'AutoCAD': {'left': 0, 'right': 0, 'middle': 0},
        'Revit': {'left': 0, 'right': 0, 'middle': 0}
    }
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            for app in ['AutoCAD', 'Revit']:
                app_df = df[df['app'] == app]
                if not app_df.empty:
                    last = app_df.iloc[-1]
                    counts[app]['left'] = int(last['left'])
                    counts[app]['right'] = int(last['right'])
                    counts[app]['middle'] = int(last['middle'])
        except Exception as e:
            print(f"讀取歷史資料失敗，將從 0 開始：{e}")
    return counts

counts = load_last_counts()
counts_history = []

# 鎖定多執行緒安全
lock = threading.Lock()

# 資料儲存檔案
DATA_FILE = 'mouse_clicks_log.csv'

# 取得目前前景視窗標題
def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

# 判斷目前是否在目標應用程式
def get_current_app():
    title = get_active_window_title()
    for app in TARGET_APPS:
        if app in title:
            return app
    return None

def is_target_app():
    return get_current_app() is not None

# 滑鼠事件處理
def on_click(x, y, button, pressed):
    if pressed:
        app = get_current_app()
        if app in TARGET_APPS:
            with lock:
                if button == mouse.Button.left:
                    counts[app]['left'] += 1
                elif button == mouse.Button.right:
                    counts[app]['right'] += 1
                elif button == mouse.Button.middle:
                    counts[app]['middle'] += 1
                # 記錄每次點擊，包含 app
                counts_history.append({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'window': get_active_window_title(),
                    'app': app,
                    'button': str(button),
                    'left': counts[app]['left'],
                    'right': counts[app]['right'],
                    'middle': counts[app]['middle']
                })

# 定時儲存資料
def save_data():
    while True:
        time.sleep(30)  # 每 30 秒儲存一次
        with lock:
            if counts_history:
                df = pd.DataFrame(counts_history)
                if os.path.exists(DATA_FILE):
                    df.to_csv(DATA_FILE, mode='a', header=False, index=False)
                else:
                    df.to_csv(DATA_FILE, index=False)
                counts_history.clear()

# 顯示統計圖表
def show_report():
    with lock:
        def app_block(app):
            l = counts[app]['left']
            r = counts[app]['right']
            m = counts[app]['middle']
            s = l + r + m
            lines = [
                f"{app} Total Clicks",
                f"RIGHT    MIDDLE   LEFT",
                f"{r:<8} {m:<8} {l:<8}",
                f"SUM: {s}"
            ]
            return '\n'.join(lines)
        print(app_block('AutoCAD'))
        print()
        print(app_block('Revit'))


# 熱鍵觸發（F12 顯示統計圖表）
def listen_keyboard():
    try:
        import keyboard
    except ImportError:
        print('如需啟用 F12 報表，請先安裝 keyboard 套件：pip install keyboard')
        return
    while True:
        keyboard.wait('f12')
        show_report()

if __name__ == '__main__':
    print('滑鼠點擊監控啟動中...\n僅統計 AutoCAD/Revit 前景視窗的點擊。\n按 F12 可隨時顯示統計圖表。\nCtrl+C 可結束程式。')
    # 啟動資料儲存執行緒
    threading.Thread(target=save_data, daemon=True).start()
    # 啟動熱鍵監聽執行緒
    threading.Thread(target=listen_keyboard, daemon=True).start()
    # 啟動滑鼠監控
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
