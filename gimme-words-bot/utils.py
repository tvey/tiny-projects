from typing import Literal


def generate_words(
    count: int | None = 100, mode: Literal["Р", "Рь", "Микс", None] = None
) -> list[str]:
    import random

    words = [
        "рад",
        "раз",
        "рыть",
        "рысь",
        "род",
        "роль",
        "руль",
        "рубль",
        "ряд",
        "рябь",
        "рис",
        "риф",
        "речь",
        "рейс",
        "рёв",
        "рюш",
    ]

    if count:
        return [random.choice(words) for _ in range(count)]

    return words
