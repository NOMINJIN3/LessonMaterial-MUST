with open("reviews.txt", "r", encoding="utf-8") as file: 
    reviews = file.readlines() 
 
results = [] 
 
for review in reviews: 
    text = review.lower() 
    positive_count = sum(word in text for word in positive_words) 
    negative_count = sum(word in text for word in negative_words) 
 
    if positive_count > negative_count: 
        sentiment = "Positive" 
    elif negative_count > positive_count: 
        sentiment = "Negative" 
    else: 
        sentiment = "Neutral" 
 
    results.append((review.strip(), sentiment)) 
 
with open("results.txt", "w", encoding="utf-8") as file: 
    for review, sentiment in results: 
        file.write(review + " -> " + sentiment + "\n") 
 
print("Шинэ review-үүдийг дахин шинжилж дууслаа.") 
