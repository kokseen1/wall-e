from random import randint
from time import sleep


def randsleep(low, hi):
    """
    Sleep for a random amount within the range given
    """
    n = randint(low, hi)
    print(f"[SLEEPING] for {n}s")
    sleep(n)
