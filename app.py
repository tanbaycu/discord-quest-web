import os
import random
from flask import Flask, render_template, request, jsonify
from core import DiscordAPI, StatelessQuestCompleter, fetch_latest_build_number, get_quest_name, get_task_type, get_seconds_needed, get_seconds_done

app = Flask(__name__)

# Global cache for build number to speed up Vercel execution
cached_build_number = None

def get_build_number():
    global cached_build_number
    if not cached_build_number:
        # Dummy log function for fetch
        cached_build_number = fetch_latest_build_number(lambda msg, level: None)
    return cached_build_number

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/quest/init", methods=["POST"])
def init_quest():
    data = request.json
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required", "status": "error"}), 400

    build_number = get_build_number()
    api = DiscordAPI(token, build_number, lambda msg, level: None)
    
    if not api.validate_token():
        return jsonify({"error": "Token không hợp lệ", "status": "error"}), 401

    completer = StatelessQuestCompleter(api)
    active_quest = completer.get_actionable_quest()
    
    if not active_quest:
        return jsonify({"status": "no_quests", "message": "Không có quest nào cần làm lúc này."})
        
    task_type = get_task_type(active_quest)
    name = get_quest_name(active_quest)
    needed = get_seconds_needed(active_quest)
    done = get_seconds_done(active_quest)
    qid = active_quest["id"]
    
    # Pre-generate stream key for games
    pid = random.randint(1000, 30000)
    stream_key = f"call:0:{pid}" if "DESKTOP" in task_type else "call:0:1"
    
    return jsonify({
        "status": "active",
        "quest": {
            "id": qid,
            "name": name,
            "task_type": task_type,
            "needed": needed,
            "done": done,
            "stream_key": stream_key
        }
    })

@app.route("/api/quest/progress_video", methods=["POST"])
def progress_video():
    data = request.json
    token = data.get("token")
    qid = data.get("id")
    timestamp = data.get("timestamp")
    
    if not token or not qid or timestamp is None:
        return jsonify({"error": "Missing params"}), 400
        
    build_number = get_build_number()
    api = DiscordAPI(token, build_number, lambda msg, level: None)
    completer = StatelessQuestCompleter(api)
    
    res = completer.send_video_progress(qid, timestamp)
    completed = bool(res.get("completed_at"))
    
    return jsonify({
        "status": "ok",
        "completed": completed
    })

@app.route("/api/quest/heartbeat", methods=["POST"])
def progress_heartbeat():
    data = request.json
    token = data.get("token")
    qid = data.get("id")
    stream_key = data.get("stream_key")
    task_type = data.get("task_type")
    
    if not token or not qid or not stream_key or not task_type:
        return jsonify({"error": "Missing params"}), 400
        
    build_number = get_build_number()
    api = DiscordAPI(token, build_number, lambda msg, level: None)
    completer = StatelessQuestCompleter(api)
    
    res = completer.send_heartbeat(qid, stream_key, terminal=False)
    
    completed = bool(res.get("completed_at"))
    new_done = -1
    pd = res.get("progress", {})
    if pd and task_type in pd:
        new_done = pd[task_type].get("value", -1)
        
    return jsonify({
        "status": "ok",
        "completed": completed,
        "done": new_done
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)

