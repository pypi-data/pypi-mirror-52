from typing import Dict, Any, List

from pydantic import BaseModel


class Links(BaseModel):
    self: str
    related: Dict


class Author(BaseModel):
    _links: Links

    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    is_admin: bool
    is_available: bool
    is_blocked: bool


class IncomingMessage(BaseModel):
    id: str
    type: str
    is_inbound: bool
    created_at: float
    blurb: str
    body: str
    text: str
    is_draft: bool
    error_type: Any
    metadata: Dict

    author: Author
    _links: Links
    recipients: List[Dict]
    attachments: List[Any]


sample = {
    "_links": {
        "self": "https://api2.frontapp.com/messages/msg_5rke22w",
        "related": {
            "conversation": "https://api2.frontapp.com/conversations/cnv_35kvnd4"
        },
    },
    "id": "msg_5rke22w",
    "type": "custom",
    "is_inbound": False,
    "created_at": 1568121811.334,
    "blurb": "test ",
    "body": "test<br>",
    "text": "test\n",
    "is_draft": True,
    "error_type": None,
    "metadata": {"headers": {"in_reply_to": "a13646cdd57640b8"}},
    "author": {
        "_links": {
            "self": "https://api2.frontapp.com/teammates/tea_1ghhk",
            "related": {
                "inboxes": "https://api2.frontapp.com/teammates/tea_1ghhk/inboxes",
                "conversations": "https://api2.frontapp.com/teammates/tea_1ghhk/conversations",
            },
        },
        "id": "tea_1ghhk",
        "email": "mb@blaster.ai",
        "username": "mb",
        "first_name": "Mikhail",
        "last_name": "Beliansky",
        "is_admin": True,
        "is_available": True,
        "is_blocked": False,
    },
    "recipients": [
        {
            "_links": {"related": {"contact": None}},
            "handle": "7a4bde8bde47ac02",
            "role": "from",
        },
        {
            "_links": {"related": {"contact": None}},
            "handle": "some_handle",
            "role": "to",
        },
    ],
    "attachments": [],
}
