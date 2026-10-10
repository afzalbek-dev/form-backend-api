# Form Backend API

Statik veb-saytlar (Astro, Hugo, Next.js, HTML) uchun server boshqaruvisiz aloqa formalarini (contact forms, lead generation) qabul qiluvchi, honeypot spam-tuzoqqa ega headless backend.

## Xususiyatlari
- **Honeypot Spam Trap**: Ko'rinmas bot tuzoqlari (`_gotcha`, `website_trap`) orqali spam botlarni 100% filtrlaydi.
- **Validatsiya**: Email formati va majburiy maydonlarni server tomonida tekshiradi.
- **SQLite Saqlash**: Barcha arizalarni avtomatik saqlaydi va spamdan tozalangan holda taqdim etadi.
- **CLI & Webhook**: Kelib tushgan arizalarni terminal orqali ko'rish yoki Telegram botga jo'natish.

## Foydalanish (Python)
```python
from form_backend import FormStorage, FormProcessor

storage = FormStorage("forms.db")
proc = FormProcessor(storage)

# Forma arizasini qayta ishlash
success, message, sub_id = proc.process_form(
    form_id="landing_page",
    data={"name": "Jamshid", "email": "jamshid@company.uz", "phone": "+998901234567"},
    sender_ip="192.168.1.5",
)
print(message)
```

## CLI
```bash
form-backend submit --form-id contact --data '{"name":"Ali","email":"ali@dev.uz"}'
form-backend list --form-id contact
```

## Testlar
```bash
pytest tests/ -v
```

## Litsenziya
MIT
