import shutil
with open('file.txt', 'a') as f:
shutil.copyfileobj(source_file, f)
# with хэллэгийг ашиглан файлд өгөгдөл нэмэх аруудыг харуулах програм
L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
# Файлд бичих
with open("myfile.txt", "w") as file1:
# Writing data to a file
file1.write("Hello \n")
file1.writelines(L)
# Файлд бичих
with open("myfile.txt", 'a') as file1:
file1.write("Today")
# Reading from file
with open("myfile.txt", "r+") as file1:
# Файлаас унших
print(file1.read())
