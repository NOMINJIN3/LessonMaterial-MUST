remove_review = "The service was okay, nothing special." 
 
with open("reviews.txt", "r", encoding="utf-8") as file: 
    reviews = file.readlines() 
 
reviews = [ 
    review for review in reviews 
    if review.strip() != remove_review 
] 
 
with open("reviews.txt", "w", encoding="utf-8") as file: 
    file.writelines(reviews) 
 
print("Сонгосон review устгагдлаа.") 
