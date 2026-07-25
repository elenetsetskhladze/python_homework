import threading


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True

    
def check_num(n):
    result = is_prime(n)
    print(f"{n} -> {result}")

num_list = [17, 25, 74, 199, 101, 41, 39, 50, 20, 19, 51]

threads = []

for n in num_list:
    thread = threading.Thread(target=check_num, args=(n,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()