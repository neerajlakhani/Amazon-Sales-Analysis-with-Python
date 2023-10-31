#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# some comment
# In[266]:


amazon = pd.read_csv('Amazon Sale Report.csv')


# ## First Understanding the data

# In[267]:


amazon.info()


# In[268]:


amazon.columns


# In[269]:


pd.set_option('display.max_columns', 30)


# In[270]:


amazon.head(1)


# In[271]:


amazon.drop(columns = ['index', 'Courier Status', 'Order ID', 'Style', 'SKU', 'currency', 'ship-country', 'Unnamed: 22'], inplace = True)


# In[272]:


amazon.isnull().sum()


# In[273]:


# Dropping the columns with percentage of null values higher than 30


# In[274]:


def drop_columns_with_high_null_percentage(df, threshold=30):
    for column in df.columns:
        if df[column].isnull().sum() / len(df) * 100 >= threshold:
            df.drop(columns=column, inplace=True)

drop_columns_with_high_null_percentage(amazon, threshold=30)

amazon.head()


# In[275]:


amazon.loc[amazon['Amount'].isnull()].head() #We can see that only those values are NaN where orders were cancelled we can replace the 


# In[276]:


amazon['Amount'].fillna(0, inplace = True)


# In[277]:


amazon['Amount'].value_counts()


# ##  Cleaning & Analyzing Data

# In[278]:


#first analyzing and visualizing only fullfilments of Amazon which were shipped or cancelled


# In[279]:


amazon['Status'].value_counts()


# In[282]:


amazon.rename(columns = {'Category':'Product Category'}, inplace =True )


# In[284]:


amazon['Date'] = pd.to_datetime(amazon['Date'])


# In[285]:


amazon['month'] = amazon['Date'].dt.month


# In[286]:


amazon['month'].value_counts()


# In[287]:


march_dates = amazon['Date'][amazon['Date'].dt.month == 3]

# Get the number of unique days in March
march_dates.dt.day.nunique()


# In[288]:


#As only there is shopping only on a single day of March, we can drop it for analysis
amazon = amazon[(amazon['Date'].dt.month != 3)]


# In[289]:


month_mapping = {
    4: 'April',
    5: 'May',
    6: 'June'
}

amazon['month'] = amazon['month'].replace(month_mapping)


# In[297]:


#we need to have months in order
month_order = ['April', 'May', 'June']
amazon['month'] = pd.Categorical(amazon['month'], categories = month_order, ordered = True)


# In[365]:


amazon.groupby('month')['Amount'].sum().sort_values(ascending=True).plot(kind = 'barh')
plt.title('Descreasing Revenue by Months')
plt.xlabel('Amount')
plt.ylabel('Months')
plt.show()


# In[447]:


# Checking the percentage of orders which were shipped and cancelled by Amazon Users
orders_shipped = amazon[(amazon['Fulfilment'] == 'Amazon') & (amazon['Status'] == 'Shipped')]
order_cancelled = amazon[(amazon['Fulfilment'] == 'Amazon') & (amazon['Status'] == 'Cancelled')]
percent_orders_shipped = len(orders_shipped)/len(amazon[amazon['Fulfilment'] == 'Amazon']) * 100
percent_orders_cancelled = len(order_cancelled)/len(amazon[amazon['Fulfilment'] == 'Amazon']) * 100
print(f'The percentage of orders shipped is {percent_orders_shipped :.2f}%, which is very high as compared to {percent_orders_cancelled:.2f} percent of orders cancelled')


# In[415]:


amazon[amazon['Fulfilment'] == 'Amazon'].groupby('Status')['Status'].count().plot(kind = 'pie')


# In[290]:


amazon['ship-city'].fillna('unknown', inplace = True)
amazon['ship-state'].fillna('unknown', inplace = True)
amazon['ship-postal-code'].fillna('unknown', inplace = True)


# In[363]:


amazon.groupby('ship-state')['Amount'].sum().sort_values(ascending = False).head().plot(kind='bar')
plt.title('Revenue Generated by States')
plt.xlabel('States')
plt.ylabel('Amount')
plt.show()


# In[373]:


amazon.groupby('Product Category')['Amount'].sum().sort_values(ascending = False).head().plot(kind='pie')


# In[414]:


df1 = amazon.groupby('Product Category')['Qty'].sum().sort_values(ascending=False).head().to_frame()
no_of_products_sold = amazon.groupby('Product Category')['Qty'].sum().sort_values(ascending=False).head()
amount_generated_products = amazon.groupby('Product Category')['Amount'].sum().sort_values(ascending=False).head()
amount_generated_by_each_product = amount_generated_products / no_of_products_sold
df2 = amount_generated_by_each_product.reset_index().rename(columns={'Product Category': 'Category', 0: 'Amount'})

df2 = df2.sort_values(by='Amount', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.bar(df1.index, df1['Qty'], color='skyblue')
ax1.set_title('Top Selling Products')
ax1.set_ylabel('Number of Products') 

ax2.bar(df2['Category'], df2['Amount'], color='lightcoral')
ax2.set_title('Amount Generated by each Product')
ax2.set_ylabel('Amount')

plt.tight_layout()
plt.show()


# In[418]:


amazon['B2B'] = amazon['B2B'].replace({True: 'Business', False: 'Individual'})


# In[446]:


customer_type_for_products = amazon.groupby('B2B')['Qty'].sum().to_frame()
custome_type_for_revenue = amazon.groupby('B2B')['Amount'].sum().to_frame()

fig, (ax1,ax2) = plt.subplots(1, 2, figsize = (12,4))
ax1.bar(customer_type_for_products.index, customer_type_for_products['Qty'], color ='skyblue')
ax1.set_title('Quantity of Products Sold by Customer Type')
ax1.set_ylabel('Number of Products')

ax2.bar(custome_type_for_revenue.index, custome_type_for_revenue['Amount'], color ='green')
ax2.set_title('Revenue Generated by Customer Type')
ax2.set_ylabel('Amount')

plt.tight_layout()
plt.show()


# # Valueable Insights

# In[448]:


# Revenue is decreasing with each month passing
# The percentage of orders shipped is 86% which is good 
# Set and Kurta are highest selling products however Western Dress and Ethnic Dress generate good revenue despite of being low selling products
# Maharashtra is the state with highest revenue
# Most number of customers are Individuals generating incomparable revenue than Business customers


# In[ ]:




