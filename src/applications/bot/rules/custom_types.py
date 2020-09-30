from typing import NamedTuple
from typing import Optional
from typing import Union


class MessageT(NamedTuple):
    chat_id: Union[str, int]
    text: str


class WebhookT(NamedTuple):
    url: str
    pending_update_count: int
    last_error_date: Optional[int]
    last_error_message: Optional[str]
    max_connections: Optional[int]
