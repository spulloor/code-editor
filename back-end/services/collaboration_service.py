from typing import Dict
from fastapi.websockets import WebSocket
import asyncio

active_sessions: Dict[str, Dict[str, WebSocket]] = {}
file_contents: Dict[str, str] = {}  # Stores the latest content of each file
file_locks: Dict[str, int] = {}  # Tracks last modification timestamp

async def add_user_to_session(session_id: str, user_id: str, websocket: WebSocket):
    await websocket.accept()
    if session_id not in active_sessions:
        active_sessions[session_id] = {}
    active_sessions[session_id][user_id] = websocket
    if session_id in file_contents:
        await websocket.send_text(file_contents[session_id])  # Send latest file state

async def remove_user_from_session(session_id: str, user_id: str):
    if session_id in active_sessions and user_id in active_sessions[session_id]:
        del active_sessions[session_id][user_id]
    if not active_sessions[session_id]:
        del active_sessions[session_id]

async def handle_edit(session_id: str, user_id: str, content: str, timestamp: int):
    last_modified = file_locks.get(session_id, 0)
    if timestamp < last_modified:
        return {"status": "conflict", "message": "Edit conflict detected. Please refresh."}
    
    file_contents[session_id] = content
    file_locks[session_id] = timestamp
    await broadcast_changes(session_id, content)
    return {"status": "success"}

async def broadcast_changes(session_id: str, message: str):
    if session_id in active_sessions:
        for websocket in active_sessions[session_id].values():
            await websocket.send_text(message)