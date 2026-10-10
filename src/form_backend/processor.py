import re
from typing import Dict, Any, Tuple, Optional
from .models import Submission
from .storage import FormStorage


class FormProcessor:
    """Forma maydonlarini tekshirish va honeypot spamini aniqlash."""

    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def __init__(self, storage: FormStorage):
        self.storage = storage

    def process_form(
        self,
        form_id: str,
        data: Dict[str, Any],
        sender_ip: str = "127.0.0.1",
    ) -> Tuple[bool, str, Optional[int]]:
        # 1. Honeypot tekshiruvi: agar bot ko'rinmas `_gotcha` yoki `website` maydonini to'ldirgan bo'lsa
        if data.get("_gotcha") or data.get("website_trap"):
            # Spam sifatida saqlaymiz, ammo botga muvaffaqiyatli deb aldaymiz
            sub_id = self.storage.save_submission(form_id, data, sender_ip, is_spam=True)
            return False, "Spam aniqlandi (Honeypot faollashdi)", sub_id

        # 2. Majburiy maydonlar va email tekshiruvi
        email = data.get("email")
        if email and not self.EMAIL_REGEX.match(str(email).strip()):
            return False, "Noto'g'ri email formati", None

        # 3. Muvaffaqiyatli saqlash
        clean_data = {k: v for k, v in data.items() if not k.startswith("_")}
        sub_id = self.storage.save_submission(form_id, clean_data, sender_ip, is_spam=False)
        return True, "Arizangiz muvaffaqiyatli qabul qilindi!", sub_id
