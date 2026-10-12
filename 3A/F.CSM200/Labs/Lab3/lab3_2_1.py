reviews = [ 
    "I love this product, it's amazing!", 
    "Worst experience ever, totally disappointed.", 
    "The service was okay, nothing special.", 
    "Absolutely fantastic! Highly recommend.", 
    "Not worth the price, I regret buying it.", 
    "Decent quality, but could be better." 
] 
 
with open("reviews.txt", "w", encoding="utf-8") as file: 
    for review in reviews: 
        file.write(review + "\n") 
 
print("reviews.txt файл үүслээ.") 
