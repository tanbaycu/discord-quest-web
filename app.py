import os
import threading
import time
from flask import Flask, render_template, request, jsonify
from datetime import datetime

from core import DiscordAPI, QuestAutocompleter, fetch_latest_build_number

app = Flask(__name__)

# Global store for bots: token -> BotManager
bots = {}

class BotManager:
    def __init__(self, token):
        self.token = token
        self.logs = []
        self.running = False
        self.thread = None
        self.completer = None

    def start(self):
        if self.running: return
        self.running = True
        self.logs = []
        self.thread = threading.Thread(target=self.run_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.log_callback("Đang yêu cầu dừng...", "warn")

    def is_running(self):
        return self.running

    def log_callback(self, msg, level="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.logs.append({"ts": ts, "msg": msg, "level": level})
        if len(self.logs) > 300:
            self.logs.pop(0)
            
    def get_logs(self, start_idx=0):
        return self.logs[start_idx:]

    def run_loop(self):
        try:
            self.log_callback("Đang khởi tạo bot...", "info")
            build_number = fetch_latest_build_number(self.log_callback)
            api = DiscordAPI(self.token, build_number, self.log_callback)
            
            if not api.validate_token():
                self.log_callback("Token không hợp lệ, dừng bot.", "error")
                self.running = False
                return
                
            self.completer = QuestAutocompleter(api, self.log_callback, self.is_running)
            
            cycle = 0
            while self.running:
                cycle += 1
                self.log_callback(f"── Quét lần #{cycle} ──", "info")
                self.completer.do_pass()
                
                # Wait before next poll
                for _ in range(60):
                    if not self.running: break
                    time.sleep(1)
                    
        except Exception as e:
            self.log_callback(f"Lỗi: {e}", "error")
        finally:
            self.running = False
            self.log_callback("Bot đã dừng.", "warn")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start_bot():
    data = request.json
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
        
    if token not in bots:
        bots[token] = BotManager(token)
        
    bot = bots[token]
    if not bot.running:
        bot.start()
        return jsonify({"message": "Started", "status": "running"})
    return jsonify({"message": "Already running", "status": "running"})

@app.route("/api/stop", methods=["POST"])
def stop_bot():
    data = request.json
    token = data.get("token")
    if not token or token not in bots:
        return jsonify({"error": "Bot not found"}), 404
        
    bot = bots[token]
    bot.stop()
    return jsonify({"message": "Stopped", "status": "stopped"})

@app.route("/api/status", methods=["GET"])
def get_status():
    token = request.args.get("token")
    if not token or token not in bots:
        return jsonify({"status": "stopped"})
    return jsonify({"status": "running" if bots[token].running else "stopped"})

@app.route("/api/logs", methods=["GET"])
def get_logs():
    token = request.args.get("token")
    start_idx = int(request.args.get("start", 0))
    if not token or token not in bots:
        return jsonify({"logs": [], "next_idx": start_idx})
        
    bot = bots[token]
    logs = bot.get_logs(start_idx)
    return jsonify({
        "logs": logs,
        "next_idx": start_idx + len(logs)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
