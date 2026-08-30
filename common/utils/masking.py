def mask_email(email: str) -> str:
    if "@" not in email:
        return "***"

    local, domain = email.split("@")
    
    if len(local) <= 1:
        masked_local = "*"
    elif len(local) == 2:
        masked_local = f"{local[0]}*"
    else:
        masked_local = f"{local[0]}{'*' * (len(local) - 2)}{local[-1]}"

    return f"{masked_local}@{domain}"