numbers = (5, -2, 7, -3, 4, -6, 8, -1)

product = 1
found = False

for i in range(len(numbers)):
    if i % 2 == 1 and numbers[i] < 0:
        product *= numbers[i]
        found = True

if found:
    print("Сондгой индекстэй сөрөг элементүүдийн үржвэр:", product)
else:
    print("Ийм элемент олдсонгүй.")
