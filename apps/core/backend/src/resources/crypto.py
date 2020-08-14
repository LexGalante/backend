from bcrypt import gensalt, hashpw, checkpw


def encrypt(text: str) -> str:
    return hashpw(text.encode('utf-8'), gensalt(12))


def validate(original: str, comparer: str) -> bool:
    return checkpw(original.encode('utf-8'), comparer.encode('utf-8'))
