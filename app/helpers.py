def validate_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) >= 10

def validate_email(email: str) -> bool:
    return "@" in email and "." in email

def format_price(price: int) -> str:
    return f"{price:,} ₽"
