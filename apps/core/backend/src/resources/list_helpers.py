from typing import List


def prevent_duplicate_items(items: List[str], new_items: str | List[str]):
    if type(new_items) is list:
        return items.append([i for i in items if i not in items])
    else:
        if new_items not in items:
            items.append(new_items)
