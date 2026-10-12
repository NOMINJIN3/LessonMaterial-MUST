# with хэллэг ашиглан файлд өгөгдөл нэмэх аргыг харуулах программ 

L = ["This is Delhi \n", "This is Paris \n", "This is London \n"] 

# Файлд бичих 

with open("myfile.txt", "w") as file1: 

    # Writing data to a file 

    file1.write("Hello \n") 

    file1.writelines(L) 

# Файлд нэмэх 

with open("myfile.txt", "a") as file1: 

    file1.write("Today") 

# Reading from file 

with open("myfile.txt", "r+") as file1: 

    # Файлаас унших 

    print(file1.read()) 
