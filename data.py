import pandas as pd

data = {
    "Name": ["Amit", "Rahul", "Neha"],
    "Age": [30, 28, 25],
    "City": ["Delhi", "Mumbai", "Pune"]
}

df = pd.DataFrame(data)

print(df)