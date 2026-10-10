import pytest
from form_backend.storage import FormStorage
from form_backend.processor import FormProcessor


def test_form_submission_success(tmp_path):
    db_file = str(tmp_path / "forms_test.db")
    storage = FormStorage(db_file)
    proc = FormProcessor(storage)

    payload = {
        "name": "Rustam Karimov",
        "email": "rustam@example.com",
        "message": "Hamkorlik bo'yicha taklif",
    }
    ok, msg, sub_id = proc.process_form("contact", payload)
    assert ok is True
    assert sub_id == 1

    subs = storage.get_submissions("contact")
    assert len(subs) == 1
    assert subs[0].data["name"] == "Rustam Karimov"
    assert subs[0].is_spam is False
    storage.close()


def test_honeypot_spam_trap():
    storage = FormStorage(":memory:")
    proc = FormProcessor(storage)

    # Bot tomonidan to'ldirilgan yashirin honeypot maydoni
    bot_payload = {
        "name": "Bot Spammer",
        "email": "bot@spam.com",
        "_gotcha": "I am a robot",
    }
    ok, msg, sub_id = proc.process_form("contact", bot_payload)
    assert ok is False
    assert "Honeypot" in msg

    # Spam hisoblanib saqlanganini tekshirish
    all_subs = storage.get_submissions("contact", include_spam=True)
    assert len(all_subs) == 1
    assert all_subs[0].is_spam is True

    # Standart ro'yxatda spam ko'rinmasligi kerak
    clean_subs = storage.get_submissions("contact", include_spam=False)
    assert len(clean_subs) == 0


def test_invalid_email_format():
    storage = FormStorage(":memory:")
    proc = FormProcessor(storage)
    ok, msg, sub_id = proc.process_form("contact", {"email": "not-an-email"})
    assert ok is False
    assert "email formati" in msg
