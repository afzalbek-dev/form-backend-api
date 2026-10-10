from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class FormConfig:
    form_id: str
    name: str
    allowed_origin: str = "*"
    webhook_url: Optional[str] = None


@dataclass
class Submission:
    id: int
    form_id: str
    data: Dict[str, Any]
    sender_ip: str
    is_spam: bool
    created_at: float
