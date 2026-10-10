"""
Form Backend API - Statik saytlar uchun spamsiz forma qabul qilish va webhook tizimi.
"""

from .models import Submission, FormConfig
from .storage import FormStorage
from .processor import FormProcessor

__version__ = "1.0.0"
__all__ = ["Submission", "FormConfig", "FormStorage", "FormProcessor"]
