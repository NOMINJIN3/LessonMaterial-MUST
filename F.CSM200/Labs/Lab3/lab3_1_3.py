ai_dictionary = { 
    "хиймэл оюун ухаан": "Artificial Intelligence", 
    "машин сургалт": "Machine Learning", 
    "гүн сургалт": "Deep Learning", 
    "нейрон сүлжээ": "Neural Network", 
    "өгөгдөл": "Data", 
    "алгоритм": "Algorithm", 
    "загвар": "Model", 
    "сургалт": "Training", 
    "туршилт": "Testing", 
    "таамаглал": "Prediction", 
    "компьютерийн хараа": "Computer Vision", 
    "байгалийн хэл боловсруулалт": "Natural Language Processing" 
} 
 
word = input("Монгол нэр томьёо оруулна уу: ").lower() 
 
if word in ai_dictionary: 
    print("Англи орчуулга:", ai_dictionary[word]) 
else: 
    print("Тольд байхгүй байна.") 
