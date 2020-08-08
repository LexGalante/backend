from typing import List


def replace_all(text: str, placeholder: str, charToRemove: List[str]):
    for char in charToRemove:
        text.replace(char, placeholder)

    return text
