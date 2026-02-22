import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def clean_data():
# Load
    df = pd.read_excel(r"C:\Users\Shubm\OneDrive\Desktop\shubham\AI_Price_Optima\retail_store_inventory.csv.xlsx")


    # Convert Date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop critical missing
    critical_cols = ['Date','Store ID','Product ID','Price','Units Sold']
    df = df.dropna(subset=critical_cols)

    # Remove duplicates
    df = df.drop_duplicates(subset=['Store ID','Product ID','Date'])

    # Remove invalid values
    df = df[df['Price'] > 0]
    df = df[df['Units Sold'] >= 0]
    df = df[df['Inventory Level'] >= 0]


    num_cols = df.select_dtypes(include=np.number).columns
    # Fill numerical columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())


    # Fill categorical columns with mode
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])


    # Create revenue
    df['Revenue'] = df['Price'] * df['Units Sold']

    # Define output path
    output_path = r"C:\Users\Shubm\OneDrive\Desktop\shubham\AI_Price_Optima\retail_store_inventory_cleaned.csv"

    # Save cleaned dataset
    df.to_csv(output_path, index=False)

    #df.info()
    #print(f"Cleaned dataset saved at: {output_path}")

    print("Cleaning Completed Successfully")


if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\Shubm\OneDrive\Desktop\shubham\AI_Price_Optima\retail_store_inventory_cleaned.csv")

    #BASICS

    # print(df.shape)
    # print(df.head())
    # df.info()
    # df.describe()

    #UNIQUE VALUES

    print("Stores:", df['Store ID'].nunique())
    print("Products:", df['Product ID'].nunique())
    print("Categories:", df['Category'].nunique())
    print("Regions:", df['Region'].nunique())

    #Revenue Analysis

    print("Total Revenue:", df['Revenue'].sum())
    df.groupby('Category')['Revenue'].sum().sort_values(ascending=False).plot(kind='bar')
    plt.title("Revenue by Category")
    plt.show()

    #Price vs Demand
    sns.scatterplot(x='Price', y='Units Sold', data=df)
    plt.title("Price vs Units Sold")
    plt.show()
    print(df[['Price','Units Sold']].corr())



    #Price Elasticity Analysis(E)
    df_sorted = df.sort_values('Price')

    df_sorted['pct_change_price'] = df_sorted['Price'].pct_change()
    df_sorted['pct_change_demand'] = df_sorted['Units Sold'].pct_change()

    # Remove zero price change
    df_sorted = df_sorted[df_sorted['pct_change_price'] != 0]

    df_sorted['elasticity'] = (
        df_sorted['pct_change_demand'] / df_sorted['pct_change_price']
    )

    # Remove inf and NaN
    df_sorted = df_sorted.replace([np.inf, -np.inf], np.nan)
    df_sorted = df_sorted.dropna(subset=['elasticity'])

    print("Average Elasticity:", df_sorted['elasticity'].mean())


    #Logistic Elasticity
    df['log_price'] = np.log(df['Price'])
    df['log_demand'] = np.log(df['Units Sold'] + 1)

    elasticity = df[['log_price','log_demand']].corr().iloc[0,1]
    print("Elasticity (log approx):", elasticity)


    # Competitor Analysis

    sns.scatterplot(x='Competitor Pricing', y='Units Sold', data=df)
    plt.title("Competitor Price vs Units Sold")
    plt.show()
    print(df[['Competitor Pricing','Units Sold']].corr())


    #Inventory Analysis

    sns.scatterplot(x='Inventory Level', y='Units Sold', data=df)
    plt.title("Inventory vs Units Sold")
    plt.show()


    #Discount Effect
    sns.boxplot(x='Discount', y='Units Sold', data=df)
    plt.title("Discount vs Units Sold")
    plt.show()

    #Time and Seasonality Analysis 
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date'])

    df['Month'] = df['Date'].dt.month

    df.groupby('Month')['Units Sold'].mean().plot()
    plt.title("Average Monthly Sales")
    plt.show()


    #Holiday and promotion
    sns.boxplot(x='Holiday/Promotion', y='Units Sold', data=df)
    plt.show()

    #Correlation Heatmap 
    plt.figure(figsize=(10,6))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
    plt.show()

    # segmente level Elasticity
    for category in df['Category'].unique():
        sub = df[df['Category'] == category]
        corr = sub[['Price','Units Sold']].corr().iloc[0,1]
        print(f"{category} elasticity proxy (corr): {corr}")




