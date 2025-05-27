import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SRC = r"D:\CascadeProjects\mouse-clicks-tool"
DST = r"D:\GitHub\chhsu01.github.io"

def sync_project(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print("同步完成！")

class SyncAndPushHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print("偵測到檔案變動，開始同步並 push...")
        sync_project(SRC, DST)
        os.system(f'cd /d "{DST}" && git add . && git commit -m "Auto sync and push" && git push origin main')

if __name__ == "__main__":
    event_handler = SyncAndPushHandler()
    observer = Observer()
    observer.schedule(event_handler, SRC, recursive=True)
    observer.start()
    print("監控中，按 Ctrl+C 結束...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()