import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

# 加载环境
load_dotenv()

# 配置
WATCH_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not WATCH_PATH.endswith("iflow_workspace"):
    WATCH_PATH = "/Users/neverdie/iflow_workspace"

DEBOUNCE_TIME = 15  # 增加抖动过滤时长
IGNORE_PATTERNS = [".git", "__pycache__", ".gemini", ".claude", ".DS_Store", "node_modules"]

class SyncHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_trigger = 0

    def on_any_event(self, event):
        if event.is_directory or any(pattern in event.src_path for pattern in IGNORE_PATTERNS):
            return
        
        current_time = time.time()
        if current_time - self.last_trigger > DEBOUNCE_TIME:
            print(f"检测到变更: {os.path.basename(event.src_path)}，准备同步...")
            self.sync_to_github()
            self.last_trigger = current_time

    def get_current_branch(self):
        try:
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
            return branch if branch else "master"
        except:
            return "master"

    def sync_to_github(self):
        try:
            os.chdir(WATCH_PATH)
            branch = self.get_current_branch()
            
            # 执行 Git 同步流程
            print(f"开始同步至分支: {branch}")
            subprocess.run(["git", "add", "."], check=True)
            
            # 检查是否有变更需要 commit
            status = subprocess.check_output(["git", "status", "--porcelain"]).decode()
            if not status:
                print("没有检测到需要提交的变更。")
                return

            commit_msg = f"🚀 Auto-sync: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            
            # 推送（假设 origin 已配置好 token）
            subprocess.run(["git", "push", "origin", branch], check=True)
            print(f"✅ 同步成功！已推送到 GitHub: {branch}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git 操作失败: {e}")
        except Exception as e:
            print(f"❌ 系统错误: {e}")

if __name__ == "__main__":
    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=True)
    observer.start()
    
    print("="*50)
    print(f"🌟 GitHub 自动同步服务已启动")
    print(f"📂 监控路径: {WATCH_PATH}")
    print(f"🌿 当前分支: {SyncHandler().get_current_branch()}")
    print("="*50)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

