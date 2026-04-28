import os
import json
from datetime import datetime
from typing import Optional


def save_message_to_txt(
    time: str,
    group_id: str,
    group_name: str,
    user_id: str,
    user_name: str,
    message: str,
    file_path: Optional[str] = None
) -> str:
    if file_path is None:
        base_dir = os.path.join(os.path.dirname(__file__), "message_logs")
        today = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(base_dir, today)
        os.makedirs(log_dir, exist_ok=True)
        file_path = os.path.join(log_dir, f"group_{group_id}.txt")
    
    log_entry = (
        f"[{time}] | "
        f"群ID: {group_id} | "
        f"群名: {group_name} | "
        f"用户ID: {user_id} | "
        f"用户名: {user_name} | "
        f"消息: {message}\n"
    )
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    return file_path


def save_message_to_yaml(
    time: str,
    group_id: str,
    group_name: str,
    user_id: str,
    user_name: str,
    message: str,
    file_path: Optional[str] = None
) -> str:
    import yaml
    
    if file_path is None:
        base_dir = os.path.join(os.path.dirname(__file__), "message_logs")
        today = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(base_dir, today)
        os.makedirs(log_dir, exist_ok=True)
        file_path = os.path.join(log_dir, f"group_{group_id}.yaml")
    
    message_data = {
        "time": time,
        "group_id": group_id,
        "group_name": group_name,
        "user_id": user_id,
        "user_name": user_name,
        "message": message,
        "saved_at": datetime.now().isoformat()
    }
    
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                existing_data = yaml.safe_load(f) or []
            except yaml.YAMLError:
                existing_data = []
    
    existing_data.append(message_data)
    
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(existing_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return file_path


def save_message(
    time: str,
    group_id: str,
    group_name: str,
    user_id: str,
    user_name: str,
    message: str,
    format_type: str = "txt",
    file_path: Optional[str] = None
) -> str:
    if format_type.lower() == "yaml":
        return save_message_to_yaml(time, group_id, group_name, user_id, user_name, message, file_path)
    else:
        return save_message_to_txt(time, group_id, group_name, user_id, user_name, message, file_path)
