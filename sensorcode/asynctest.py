from time import sleep

def counter(x):
    for i in range(x):
        sleep(1)
        yield i

for num in counter(5):
    print(num)
