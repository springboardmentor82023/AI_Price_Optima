import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1) Load dataset
df = pd.read_csv("../data/raw/amazon_sales_dataset.csv")
print("Shape of dataset:", df.shape)
print("\nColumns:", df.columns)
print("\nInfo:")
df.info()
print("view the data converted inn dataframe (table format)")
print(df.head()) # view the data converted inn dataframe (table format)
print("Each row price for entire respected column")
print(df['price'])

# 2) Check duplicate rows
duplicates = df.duplicated().sum()
print("\nNumber of duplicate rows:", duplicates)
df.groupby('product_category')['total_revenue'].sum()

# 3) Remove duplicates
df = df.drop_duplicates()
print("Duplicates removed. New shape:", df.shape)

# 4) Check missing values
print("\nMissing values in each column:\n")
print(df.isnull().sum())

# 5) Remove rows null values (if any)
df = df.dropna()
print("\nAfter removing null rows:")
print(df.isnull().sum())

# 6) Fix data types
df['order_date'] = pd.to_datetime(df['order_date'])
df['price'] = df['price'].astype(float)
df['quantity_sold'] = df['quantity_sold'].astype(int)

# 7) Basic validation checks
print("\nFinal dataset shape:", df.shape)
print("\nAny duplicates left:", df.duplicated().sum())
print("\nAny null values left:\n", df.isnull().sum())

# 8) Save cleaned dataset
df.to_csv("data/processed/amazon_sales_cleaned.csv", index=False)

print("\nData preprocessing completed successfully.")

# Convert column to numpy array
'''
price_array = np.array(df['price'])
print("Mean of the price column: ", np.mean(price_array))
print("Median of the price column: ", np.median(price_array))
print("Mode of the price column: ", np.std(price_array))

# Sales trend - graphs
plt.plot(df['total_revenue'])
plt.title("Revenue Trend")
plt.xlabel("Orders")
plt.ylabel("Revenue")
plt.show()

# Category vs revenue
sns.barplot(x='product_category', y='total_revenue', data=df)
plt.xticks(rotation=45)
plt.show()'''