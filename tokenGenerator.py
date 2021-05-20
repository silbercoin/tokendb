import random
import string
import csv


def randomToken(length=7, uppercase=False, lowercase=True, numbers=True):
    token = ''

    if lowercase:
        token += string.ascii_lowercase

    return ''.join(random.choice(token) for i in range(length))


with open('tokens.csv', 'w', newline='') as f:
    token = csv.writer(f)
    token.writerow(['token'])

    n = 10000000
    for i in range(0, n):
        tokenSet = randomToken()
        token.writerow([tokenSet])
