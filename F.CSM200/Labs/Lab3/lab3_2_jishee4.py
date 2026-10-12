# Import necessary libraries 

with open("reviews.txt", "r") as file: 

    reviews = file.readlines()  # Файлын бүх мөрийг уншина. 

 

# Define simple keyword-based sentiment analysis 

positive_words = ["love", "amazing", "fantastic", "recommend", "great"] 

negative_words = ["worst", "disappointed", "not worth", "regret", "bad"] 

 

results = [] 

 

for review in reviews: 

    review_lower = review.lower()  # Том үсгийг жижиг үсгээр хөрвүүлнэ 

    if any(word in review_lower for word in positive_words): 

        sentiment = "Positive" 

    elif any(word in review_lower for word in negative_words): 

        sentiment = "Negative" 

    else: 

        sentiment = "Neutral" 

 

    results.append(f"{review.strip()} -> Sentiment: {sentiment}") 

 

# Үр дүнг шинэ файлд хадгална 

with open("results.txt", "w") as output_file: 

    for result in results: 

        output_file.write(result + "\n") 

 

print("Sentiment analysis complete! Check 'results.txt' for results.") 
