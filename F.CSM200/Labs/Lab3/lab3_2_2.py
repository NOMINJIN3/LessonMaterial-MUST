positive_words = [ 
    "good", "great", "excellent", "love", "best", 
    "happy", "amazing", "fantastic", "recommend", 
    "decent" 
] 
 
negative_words = [ 
    "bad", "terrible", "worst", "hate", "poor", 
    "disappointed", "not worth", "regret" 
] 
 
with open("reviews.txt", "r", encoding="utf-8") as file: 
    reviews = file.readlines() 
 
results = [] 
 
for review in reviews: 
    text = review.lower() 
    positive_count = 0 
    negative_count = 0 
 
    for word in positive_words: 
        if word in text: 
            positive_count += 1 
 
    for word in negative_words: 
        if word in text: 
            negative_count += 1 
 
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
 
print("Sentiment analysis дууслаа.") 
