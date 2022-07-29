
import random

ALPHA_UPPERS = {chr(ord('A') + i) for i in range(ord('Z') - ord('A') + 1)}
ALPHA_LOWER = {chr(ord('a') + i) for i in range(ord('z') - ord('a') + 1)}
DIGITS = {chr(ord('0') + i) for i in range(ord('9') - ord('0') + 1)}
ALNUM = list(ALPHA_UPPERS | ALPHA_LOWER | DIGITS)


def get_random_string(length: int) -> str:
    return ''.join((random.choice(ALNUM) for _ in range(length)))
