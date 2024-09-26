from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from database import get_db
from websocket_manager import wsok_manager

router = APIRouter(prefix="/ws", tags=["ws"])


def get_user_id_from_token():
    return 1


@router.websocket("")
async def connect(websocket: WebSocket, user_id=Depends(get_user_id_from_token)):
    await websocket.accept()
    # await wsok_manager.connect(websocket, user_id)
    # await wsok_manager.ping(websocket)
    # await wsok_manager.pong(websocket)
