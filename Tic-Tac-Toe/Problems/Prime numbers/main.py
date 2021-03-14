prime_numbers = []
for i in range(2, 1000):
    divisible = []
    for j in range(2,i):
        divisible.append(i % j == 0 and i / j != 1)
    if any(divisible):
        continue
    else:
        prime_numbers.append(i)
