import matplotlib.pyplot as plt
import pandas as pd

#plt.plot([1, 2, 3, 4])
#plt.show()

x = [1, 2, 3, 4]
y = [10, 20, 15, 30]

#plt.plot(x, y)
#plt.show()

# departments = ["IT", "HR", "Sales", "Finance"]
# employees = [50, 20, 40, 15]

# plt.bar(departments, employees)

# plt.show()

# departments = ["IT", "HR", "Sales", "Finance"]
# employees = [50, 20, 40, 15]

# plt.pie(
#     employees,
#     labels=departments,
#     autopct="%1.1f%%"
# )

# plt.show()

# age = [20, 25, 30, 35, 40]
# salary = [25000, 35000, 50000, 65000, 80000]

# plt.scatter(age, salary)

# plt.show()

# ages = [
#     22, 25, 27, 28, 30,
#     31, 32, 35, 36, 40,
#     42, 45
# ]

# plt.hist(ages)



# plt.savefig("monthly_sales.pdf")

# plt.show()

df = pd.DataFrame({
    "Department": ["IT", "HR", "Sales", "Finance"],
    "Employees": [50, 20, 40, 15]
})

plt.bar(
    df["Department"],
    df["Employees"]
)

plt.xlabel("Department")
plt.ylabel("Employees")
plt.title("Employees by Department")

plt.show()
