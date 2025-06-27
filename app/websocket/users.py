from typing import Dict, Annotated

from fastapi import APIRouter, WebSocket, Depends, Path

from app.db.users import db_actions
from app.db.users.models import User


websocket_route = APIRouter(prefix="/ws")
connections: Dict[str, WebSocket] = {}

@websocket_route.websocket("/{friend_name}/{token}/")
# username: Annotated[str, Depends(db_actions.decode_jwt)],
async def web_socket_server(websocket: WebSocket, friend_name: str = Path(...), token: str = Path(...)):
    username = db_actions.get_username(token=token)
    print(f"{username = }")
    await websocket.accept()
    while True:
        text = await websocket.receive_text()
        print(text)
        await websocket.send_text(text)
    # connections.update({username: websocket})