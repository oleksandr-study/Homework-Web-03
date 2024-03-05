"""
def factorize(*number):
    # YOUR CODE HERE
    raise NotImplementedError() # Remove after implementation


a, b, c, d  = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
"""


from multiprocessing import Pool, current_process, cpu_count
from time import time

def factorize(num):
    result = []
    i = 1
    while i < num + 1:
        if num % i == 0:
            result.append(i)
        i = i + 1
    return result


def callback(result):
    print(f"Result in callback: {result}")


if __name__ == '__main__':
    print(f"Start of multiprocessing counting experiment\nSync version")
    timer = time()
    with Pool(2) as pool:
        r = pool.map(factorize, [128, 255, 99999, 10651060])
        print(r)
    print(f"Done count in {round(time() - timer, 4)} sec\n")

    print(f"Async version\nCount CPU: {cpu_count()}")
    timer = time()
    with Pool(cpu_count()) as p:
        p.map_async(
            factorize,
            [128, 255, 99999, 10651060],
            callback=callback,
        )
        p.close()  # перестати виділяти процеси в пулл
        p.join()  # дочекатися закінчення всіх процесів
    print(f"Done count in {round(time() - timer, 4)} sec\n")