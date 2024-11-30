import pandas as pd

df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [1, 2], 'B': [3, 5, 6]})

# Compare DataFrames
diff = df1.compare(df2)

# Update df1 with values from df2 where there are differences
df1.update(df2)

print(df1)