import matplotlib.pyplot as plt

products = ["Laptop", "Mouse", "Keyboard"]
sales = [50, 80, 60]

plt.bar(products, sales)

plt.xlabel("Products")
plt.ylabel("Sales")
plt.title("Product Sales")

plt.show()