 ax= revenue.plot(kind='bar')
#     plt.ylabel("Revenue (Millions)")
#     plt.title("Revenue by Category")
#     plt.ylim(100, 125) 
#     for p in ax.patches:
#         height = p.get_height()
#         ax.annotate(f'{height:.2f}',
#                     (p.get_x() + p.get_width() / 2., height),
#                     ha='center', va='bottom')
#     plt.show()


#     #Testiing 
#     sns.scatterplot(x='Weather Condition', y='Price', data=df)
#     plt.title("Weather Condition vs Price")
#     plt.show()  
#     #Price vs Demand
#     sns.scatterplot(x='Units Sold', y='Price', data=df)
#     plt.ylabel("Price")     
#     plt.xlabel("Units Sold")
#     plt.title("Price vs Units Sold")
#    # plt.ylim(350,500)
#     plt.show()

#     df_sorted = df.sort_values('Price')

#     plt.plot(df_sorted['Price'], df_sorted['Units Sold'])
#     plt.xlabel("Price")
#     plt.ylabel("Units Sold")
#     plt.title("Price vs Units Sold")
#     plt.ylim(350,500)
#     plt.show()
    
#     print()
#     print()

#     #Price Elasticity Analysis(E)
#     df_sorted = df.sort_values('Price')

#     df_sorted['pct_change_price'] = df_sorted['Price'].pct_change()
#     df_sorted['pct_change_demand'] = df_sorted['Units Sold'].pct_change()

#     # Remove zero price change
#     df_sorted = df_sorted[df_sorted['pct_change_price'] != 0]

#     df_sorted['elasticity'] = (
#         df_sorted['pct_change_demand'] / df_sorted['pct_change_price']
#     )

#     # Remove inf and NaN
#     df_sorted = df_sorted.replace([np.inf, -np.inf], np.nan)
#     df_sorted = df_sorted.dropna(subset=['elasticity'])

#    # print("Average Elasticity:", df_sorted['elasticity'].mean())


#     #Logistic Elasticity
#     df['log_price'] = np.log(df['Price'])
#     df['log_demand'] = np.log(df['Units Sold'] + 1)

#     elasticity = df[['log_price','log_demand']].corr().iloc[0,1]
#     print("Elasticity (log approx):", elasticity)


#     # Competitor Analysis

#     sns.scatterplot(x='Competitor Pricing', y='Units Sold', data=df)
#     plt.title("Competitor Price vs Units Sold")
#     plt.show()
#     print(df[['Competitor Pricing','Units Sold']].corr())


#     # #Inventory Analysis

#     sns.scatterplot(x='Inventory Level', y='Units Sold', data=df)
#     plt.title("Inventory vs Units Sold")
#     plt.show()


#     #Discount Effect
#     # sns.boxplot(x='Discount', y='Units Sold', data=df)
#     df.groupby('Discount')['Units Sold'].mean().plot(kind='bar')
#     plt.xlabel("Discount (%)")
#     plt.ylabel("Average Units Sold")
#     plt.title("Discount vs Units Sold")
#     plt.show()
    

#     #Time and Seasonality Analysis 
#     df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
#     df = df.dropna(subset=['Date'])

#     df['Month'] = df['Date'].dt.month

#     df.groupby('Month')['Units Sold'].mean().plot()
#     plt.title("Average Monthly Sales")
#     plt.show()

#     #Revenue over time
#     df.groupby('Date')['Revenue'].sum().plot()
#     plt.title(" Revenue Trend")
#     plt.show()

#     #Holiday and promotion
#     sns.boxplot(x='Holiday/Promotion', y='Units Sold', data=df)
#     plt.show()