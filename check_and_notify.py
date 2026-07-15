import json
import os
import urllib.request
from datetime import datetime, timezone

STATE_PATH = "data/state.json"


def load_state():
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def send_line_push(token, user_id, text):
    url = "https://api.line.me/v2/bot/message/push"
    body = json.dumps({"to": user_id, "messages": [{"type": "text", "text": text}]}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return resp.status


def main():
    state = load_state()

    if not state.get("active"):
        print("timer not active, nothing to do")
        return

    if state.get("notified"):
        print("already notified for this timer")
        return

    target = datetime.fromisoformat(state["target_time"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    if now >= target:
        token = os.environ["LINE_TOKEN"]
        user_id = os.environ["LINE_USER_ID"]
        send_line_push(token, user_id, "⏰ ครบกำหนดเวลาจอดรถแล้ว (3 ชั่วโมง) กรุณาตรวจสอบรถของคุณ")
        state["notified"] = True
        save_state(state)
        print("LINE notification sent")
    else:
        print(f"not due yet, {target - now} remaining")


if __name__ == "__main__":
    main()
