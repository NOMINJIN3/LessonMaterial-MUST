numbers = [12, 5, 8, 3, 17, 10, 6, 21, 4, 9]

B = []
C = []

for number in numbers:
    if number % 2 == 0:
        B.append(number)
    else:
        C.append(number)

B.sort(reverse=True)
C.sort()

print("Тэгш тоонууд B:", B)
print("Сондгой тоонууд C:", C)
