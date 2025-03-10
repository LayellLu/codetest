from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# 保存活动连接的列表，每个元素是一个字典，包含 WebSocket 对象和用户名
active_connections = []  # 示例: [{"ws": WebSocket, "username": "Alice"}, ...]

@app.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    # 接受WebSocket连接
    await websocket.accept()
    try:
        # 等待客户端发送用户名作为第一条消息
        username = await websocket.receive_text()
    except WebSocketDisconnect:
        # 如果在接收用户名前连接断开，直接结束
        return

    # 将新的连接和用户名存储起来
    active_connections.append({"ws": websocket, "username": username})
    # 广播通知所有客户端，有新用户加入
    join_message = f"{username} 加入了聊天"
    for conn in active_connections:
        await conn["ws"].send_text(join_message)

    try:
        # 持续监听来自该客户端的消息
        while True:
            # 接收客户端发送的聊天消息文本
            data = await websocket.receive_text()
            message = f"{username}: {data}"
            # 将消息广播给所有已连接的客户端
            for conn in active_connections:
                await conn["ws"].send_text(message)
    except WebSocketDisconnect:
        # 处理客户端断开连接
        # 从活动连接列表中移除该客户端
        active_connections[:] = [conn for conn in active_connections if conn["ws"] is not websocket]
        # 通知其他客户端该用户已离开
        leave_message = f"{username} 离开了聊天"
        for conn in active_connections:
            await conn["ws"].send_text(leave_message)
