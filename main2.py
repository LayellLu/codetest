from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Cookie, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Response
import uvicorn
import uuid

app = FastAPI()

fake_users_db = {
    "alice": "alice123",
    "bob": "bob123"
}

active_sessions = {}

class ConnectionManager:
    """管理 WebSocket 连接和广播消息的类"""
    def __init__(self):
        self.active_connections: dict[WebSocket, str] = {}
    
    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.pop(websocket)
    
    async def broadcast(self, message: str):
        for ws in list(self.active_connections.keys()):
            try:
                await ws.send_text(message)
            except Exception:
                self.disconnect(ws)

manager = ConnectionManager()

def authenticate_user(username: str, password: str) -> bool:
    return username in fake_users_db and fake_users_db[username] == password

def create_session(username: str) -> str:
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = username 
    return session_id


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if not authenticate_user(username, password):
        error_html = "<h2 style='color:red;'>用户名或密码错误</h2>" + login_page_html
        return HTMLResponse(error_html, status_code=401)
    session_id = create_session(username)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600 * 24 * 7 
    )
    return response

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str = Cookie(None)):
    if not session_id or session_id not in active_sessions:
        await websocket.accept()
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    username = active_sessions[session_id]
    await manager.connect(websocket, username)
    await manager.broadcast(f"用户 {username} 加入了聊天室")
    try:
        while True:
            data = await websocket.receive_text()
            message = f"{username}: {data}"
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户 {username} 离开了聊天室")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)