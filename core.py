import requests
import time
import json
import random
import base64
import re
from datetime import datetime, timezone

API_BASE = "https://discord.com/api/v9"
SUPPORTED_TASKS = [
    "WATCH_VIDEO",
    "PLAY_ON_DESKTOP",
    "STREAM_ON_DESKTOP",
    "PLAY_ACTIVITY",
    "WATCH_VIDEO_ON_MOBILE",
]

def fetch_latest_build_number(log_func) -> int:
    FALLBACK = 504649
    try:
        log_func("Đang lấy build number mới nhất từ Discord...", "info")
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        r = requests.get("https://discord.com/app", headers={"User-Agent": ua}, timeout=15)
        if r.status_code != 200:
            log_func(f"Không lấy được trang Discord ({r.status_code}), dùng fallback", "warn")
            return FALLBACK

        scripts = re.findall(r'/assets/([a-f0-9]+)\.js', r.text)
        if not scripts:
            scripts_alt = re.findall(r'src="(/assets/[^"]+\.js)"', r.text)
            scripts = [s.split('/')[-1].replace('.js', '') for s in scripts_alt]

        if not scripts:
            log_func("Không tìm thấy JS assets, dùng fallback", "warn")
            return FALLBACK

        for asset_hash in scripts[-5:]:
            try:
                ar = requests.get(
                    f"https://discord.com/assets/{asset_hash}.js",
                    headers={"User-Agent": ua}, timeout=15
                )
                m = re.search(r'buildNumber["\s:]+["\s]*(\d{5,7})', ar.text)
                if m:
                    bn = int(m.group(1))
                    log_func(f"Build number: {bn}", "ok")
                    return bn
            except Exception:
                continue

        log_func(f"Không tìm thấy build number, dùng fallback {FALLBACK}", "warn")
        return FALLBACK
    except Exception as e:
        log_func(f"Lỗi lấy build number: {e}, dùng fallback {FALLBACK}", "warn")
        return FALLBACK

def make_super_properties(build_number: int) -> str:
    obj = {
        "os": "Windows",
        "browser": "Discord Client",
        "release_channel": "stable",
        "client_version": "1.0.9175",
        "os_version": "10.0.26100",
        "os_arch": "x64",
        "app_arch": "x64",
        "system_locale": "en-US",
        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9175 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36",
        "browser_version": "32.2.7",
        "client_build_number": build_number,
        "native_build_number": 59498,
        "client_event_source": None,
    }
    return base64.b64encode(json.dumps(obj).encode()).decode()

class DiscordAPI:
    def __init__(self, token: str, build_number: int, log_func):
        self.token = token
        self.log_func = log_func
        self.session = requests.Session()
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9175 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36"
        sp = make_super_properties(build_number)
        self.session.headers.update({
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": ua,
            "X-Super-Properties": sp,
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Asia/Ho_Chi_Minh",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me",
        })

    def get(self, path: str, **kwargs) -> requests.Response:
        url = f"{API_BASE}{path}"
        r = self.session.get(url, **kwargs)
        return r

    def post(self, path: str, payload: dict = None, **kwargs) -> requests.Response:
        url = f"{API_BASE}{path}"
        r = self.session.post(url, json=payload, **kwargs)
        return r

    def validate_token(self) -> bool:
        try:
            r = self.get("/users/@me")
            if r.status_code == 200:
                user = r.json()
                name = user.get("username", "?")
                self.log_func(f"Đăng nhập: {name} (ID: {user.get('id')})", "ok")
                return True
            else:
                self.log_func(f"Token không hợp lệ (status {r.status_code})", "error")
                return False
        except Exception as e:
            self.log_func(f"Không thể kết nối tới Discord: {e}", "error")
            return False

def _get(d: dict, *keys):
    if d is None:
        return None
    for k in keys:
        if k in d:
            return d[k]
    return None

def get_task_config(quest: dict) -> dict:
    cfg = quest.get("config", {})
    return _get(cfg, "taskConfig", "task_config", "taskConfigV2", "task_config_v2")

def get_quest_name(quest: dict) -> str:
    cfg = quest.get("config", {})
    msgs = cfg.get("messages", {})
    name = _get(msgs, "questName", "quest_name")
    if name: return name.strip()
    game = _get(msgs, "gameTitle", "game_title")
    if game: return game.strip()
    app_name = cfg.get("application", {}).get("name")
    if app_name: return app_name
    return f"Quest#{quest.get('id', '?')}"

def is_completable(quest: dict) -> bool:
    tc = get_task_config(quest)
    if not tc or "tasks" not in tc: return False
    return any(tc["tasks"].get(t) is not None for t in SUPPORTED_TASKS)

def is_enrolled(quest: dict) -> bool:
    us = _get(quest, "userStatus", "user_status") or {}
    return bool(_get(us, "enrolledAt", "enrolled_at"))

def is_completed(quest: dict) -> bool:
    us = _get(quest, "userStatus", "user_status") or {}
    return bool(_get(us, "completedAt", "completed_at"))

def get_task_type(quest: dict) -> str:
    tc = get_task_config(quest)
    if not tc or "tasks" not in tc: return None
    for t in SUPPORTED_TASKS:
        if tc["tasks"].get(t) is not None: return t
    return None

def get_seconds_needed(quest: dict) -> int:
    tc = get_task_config(quest)
    task_type = get_task_type(quest)
    if not tc or not task_type: return 0
    return tc["tasks"][task_type].get("target", 0)

def get_seconds_done(quest: dict) -> float:
    task_type = get_task_type(quest)
    if not task_type: return 0
    us = _get(quest, "userStatus", "user_status") or {}
    progress = us.get("progress", {})
    return progress.get(task_type, {}).get("value", 0)

class QuestAutocompleter:
    def __init__(self, api: DiscordAPI, log_func, is_running_func):
        self.api = api
        self.log = log_func
        self.is_running = is_running_func
        self.completed_ids = set()

    def fetch_quests(self) -> list:
        try:
            r = self.api.get("/quests/@me")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict): return data.get("quests", [])
                elif isinstance(data, list): return data
            elif r.status_code == 429:
                wait = r.json().get("retry_after", 10)
                self.log(f"Rate limited – chờ {wait}s", "warn")
                time.sleep(min(wait, 5))
            return []
        except Exception as e:
            self.log(f"Lỗi lấy quests: {e}", "error")
            return []

    def enroll_quest(self, quest: dict):
        name = get_quest_name(quest)
        qid = quest["id"]
        try:
            r = self.api.post(f"/quests/{qid}/enroll", {
                "location": 11,
                "is_targeted": False,
                "metadata_raw": None,
                "metadata_sealed": None,
                "traffic_metadata_raw": quest.get("traffic_metadata_raw"),
                "traffic_metadata_sealed": quest.get("traffic_metadata_sealed"),
            })
            if r.status_code in (200, 201, 204):
                self.log(f"Đã nhận: {name}", "ok")
                return True
        except Exception as e:
            self.log(f"Lỗi nhận {name}: {e}", "error")
        return False

    def do_pass(self):
        quests = self.fetch_quests()
        if not quests:
            self.log("Không có quest nào.", "info")
            return

        # Auto accept
        for q in quests:
            if not self.is_running(): return
            if not is_enrolled(q) and not is_completed(q) and is_completable(q):
                self.enroll_quest(q)
                time.sleep(2)
                
        quests = self.fetch_quests()
        actionable = [q for q in quests if is_enrolled(q) and not is_completed(q) and is_completable(q) and q.get("id") not in self.completed_ids]

        if not actionable:
            self.log("Không có quest nào cần hoàn thành lúc này.", "info")
            return

        for q in actionable:
            if not self.is_running(): return
            self.process_quest(q)

    def process_quest(self, quest: dict):
        task_type = get_task_type(quest)
        name = get_quest_name(quest)
        qid = quest["id"]
        
        self.log(f"Bắt đầu: {name} ({task_type})", "info")
        
        if task_type in ("WATCH_VIDEO", "WATCH_VIDEO_ON_MOBILE"):
            self.complete_video(quest)
        elif task_type in ("PLAY_ON_DESKTOP", "STREAM_ON_DESKTOP", "PLAY_ACTIVITY"):
            self.complete_heartbeat(quest, task_type)
            
        self.completed_ids.add(qid)

    def complete_video(self, quest: dict):
        name = get_quest_name(quest)
        qid = quest["id"]
        needed = get_seconds_needed(quest)
        done = get_seconds_done(quest)
        
        speed = 7
        interval = 1
        
        self.log(f"🎬 Video: {name} ({done:.0f}/{needed}s)", "info")
        while done < needed and self.is_running():
            timestamp = done + speed
            try:
                r = self.api.post(f"/quests/{qid}/video-progress", {"timestamp": min(needed, timestamp + random.random())})
                if r.status_code == 200:
                    if r.json().get("completed_at"):
                        self.log(f"✅ Hoàn thành: {name}", "ok")
                        return
                    done = min(needed, timestamp)
                    self.log(f"  [{name}] {done:.0f}/{needed}s", "progress")
            except: pass
            
            if timestamp >= needed: break
            time.sleep(interval)
            
        if self.is_running():
            self.api.post(f"/quests/{qid}/video-progress", {"timestamp": needed})
            self.log(f"✅ Hoàn thành: {name}", "ok")

    def complete_heartbeat(self, quest: dict, task_type: str):
        name = get_quest_name(quest)
        qid = quest["id"]
        needed = get_seconds_needed(quest)
        done = get_seconds_done(quest)
        
        self.log(f"🎮 {task_type}: {name} (cần {needed}s)", "info")
        pid = random.randint(1000, 30000)
        stream_key = f"call:0:{pid}" if "DESKTOP" in task_type else "call:0:1"
        
        while done < needed and self.is_running():
            try:
                r = self.api.post(f"/quests/{qid}/heartbeat", {"stream_key": stream_key, "terminal": False})
                if r.status_code == 200:
                    body = r.json()
                    pd = body.get("progress", {})
                    if pd and task_type in pd:
                        done = pd[task_type].get("value", done)
                    self.log(f"  [{name}] {done:.0f}/{needed}s", "progress")
                    if body.get("completed_at") or done >= needed:
                        self.log(f"✅ Hoàn thành: {name}", "ok")
                        return
                elif r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 10))
            except: pass
            
            for _ in range(20): # HEARTBEAT_INTERVAL
                if not self.is_running(): return
                time.sleep(1)
                
        if self.is_running():
            self.api.post(f"/quests/{qid}/heartbeat", {"stream_key": stream_key, "terminal": True})
            self.log(f"✅ Hoàn thành: {name}", "ok")
