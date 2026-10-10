import argparse
import sys
import json
from .storage import FormStorage
from .processor import FormProcessor


def main():
    parser = argparse.ArgumentParser(description="Form Backend API - Statik saytlar uchun formalar qabul qilish CLI")
    parser.add_argument("--db", default="/tmp/forms.db", help="SQLite ma'lumotlar bazasi fayli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_p = subparsers.add_parser("submit", help="Forma yuborishni sinab ko'rish")
    submit_p.add_argument("--form-id", required=True)
    submit_p.add_argument("--data", required=True, help="JSON formatidagi maydonlar, masalan: '{\"name\":\"Ali\",\"email\":\"ali@mail.uz\"}'")
    submit_p.add_argument("--ip", default="127.0.0.1")

    list_p = subparsers.add_parser("list", help="Kelib tushgan arizalarni ko'rish")
    list_p.add_argument("--form-id", required=True)
    list_p.add_argument("--include-spam", action="store_true")

    args = parser.parse_args()
    storage = FormStorage(args.db)
    proc = FormProcessor(storage)

    if args.command == "submit":
        data = json.loads(args.data)
        ok, msg, sub_id = proc.process_form(args.form_id, data, sender_ip=args.ip)
        if ok:
            print(f"✅ {msg} (ID: #{sub_id})")
        else:
            print(f"❌ {msg}")
    elif args.command == "list":
        subs = storage.get_submissions(args.form_id, include_spam=args.include_spam)
        print(f"Arizalar soni: {len(subs)}")
        for s in subs:
            spam_tag = " [SPAM]" if s.is_spam else ""
            print(f"#{s.id}{spam_tag} ({s.sender_ip}): {json.dumps(s.data, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
