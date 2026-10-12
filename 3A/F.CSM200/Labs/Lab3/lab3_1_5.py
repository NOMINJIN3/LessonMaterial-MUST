fruits = [ 
    {"name": "Apple", "price": 5000}, 
    {"name": "Banana", "price": 6000}, 
    {"name": "Orange", "price": 7000}, 
    {"name": "Mango", "price": 9000} 
] 
 
def find_fruits_by_price(price): 
    result = [] 
 
    for fruit in fruits: 
        if fruit["price"] == price: 
            result.append(fruit["name"]) 
 
    return result 
 
print("Жимснүүд:") 
for fruit in fruits: 
    print(fruit["name"], "-", fruit["price"], "₮") 
 
price = int(input("\nҮнэ оруулна уу: ")) 
result = find_fruits_by_price(price) 
 
if result: 
    print("Тухайн үнэтэй жимс:", result) 
else: 
    print("Тухайн үнэтэй жимс олдсонгүй.") 
 
fruit_names = set() 
 
for fruit in fruits: 
    fruit_names.add(fruit["name"]) 
 
print("Жимсний set:", fruit_names) 
 
fruit_info = ("Apple", 5000) 
print("Tuple:", fruit_info) 
