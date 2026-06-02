# Q4:
# Given a CSV file Products.csv with columns:
# Write a Python program to:
# a) Read the CSV
# b) Print each row in a clean format
# c) Total number of rows
# d) Total number of products priced above 500
# e) Average price of all products
# f) List all products belonging to a specific category (user input)
# g) Total quantity of all items in stock


print("Program Started")
import csv
products = []
with open("product.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        products.append(row)
print("Product Details")
for product in products:
    print(product)
print("Total number of rows:", len(products))

#products price above 500
count = 0
for product in products:
    if int(product['price']) > 500:
        count += 1
print("Products priced above 500:", count)

#Average price
average = sum(int(product['price']) for product in products) / len(products)
print("Average Price:", average)

#product of specific category
category = input("Enter category: ")
found = False
for product in products:
    if product['category'].lower() == category.lower():
        print(product['product_name'])
        found = True
if not found:
    print("No products found")

#total quantity in stock
total_quantity = 0
for product in products:
    total_quantity += int(product['quantity'])

print("Total quantity in stock:", total_quantity)
    