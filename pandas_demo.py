import pandas as pd

# names = pd.Series(["Amit", "Rahul", "John", "Priya"])

# names = pd.Series(
#     ["Amit", "Rahul", "John"],
#     index=[101, 102, 103]
# )

# print(names)

# df = pd.DataFrame({
#     "Id": [1, 2, 3],
#     "Name": ["Amit", "Rahul", "John"],
#     "Age": [30, 28, 35],
#     "Salary": [50000, 60000, 70000]
# })

# print(df)

data = {
    "Name": ["Amit", "Rahul", "John"],
    "Age": [30, 28, 35],
    "Salary": [50000, 60000, 70000]
}

df = pd.DataFrame(data)

csv = pd.read_csv("./Document/pandas.csv")

#print(csv[csv["Name"]=="Amit Shukla"]);
#print(csv.loc[0:2,"Name"])
#print(csv.iloc[0:3,1:3])
#print(csv.sort_values(by="Salary", ascending=True))

employees = pd.DataFrame({
    "EmployeeId": [1, 2, 3],
    "Name": ["Amit", "Rahul",None],
    "DepartmentId": [10, 20, 10]
})

departments = pd.DataFrame({
    "DepartmentId": [10, 20],
    "DepartmentName": ["IT", "HR"]
})

result = pd.merge(employees, departments, on="DepartmentId", how="inner")
result["Name"]=result["Name"].fillna("Amit")
print(result);

df1 = pd.DataFrame({
    "Name": ["Amit", "Rahul"]
})

df2 = pd.DataFrame({
    "Name": ["John", "Priya"]
})

result = pd.concat([df1["Name"],df2["Name"]],ignore_index=True)

#print(result);