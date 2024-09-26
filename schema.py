from pydantic import BaseModel
from typing import Any


class PushNotificationInput(BaseModel):
    message: Any
    user_id: int
