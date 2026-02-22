for category in df['Category'].unique():
        sub = df[df['Category'] == category]
        corr = sub[['Price','Units Sold']].corr().iloc[0,1]
        print(f"{category} elasticity proxy (corr): {corr}")