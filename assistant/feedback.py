import json
import os
from datetime import datetime

from assistant.config import FEEDBACK_LOG


def log_feedback(message_id, feedback_data, user_msg, assistant_msg):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "message_id": message_id,
        "feedback": feedback_data["feedback"],
        "comment": feedback_data.get("text", ""),
        "user_message": user_msg,
        "assistant_response": assistant_msg,
    }
    with open(FEEDBACK_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
