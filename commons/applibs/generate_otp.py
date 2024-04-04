import random


def generate_numeric_otp(size):
    otp = ''
    for i in range(size):
        otp += str(random.randint(1, 9))
    return otp
