
# 1. Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics for plots
# %matplotlib inline
sns.set_theme(style="whitegrid")

# 2. Load the dataset using Pandas
# Ensure 'telco-customer-churn-by-contract.csv' is in the same folder as this script
df = pd.read_csv('telco-customer-churn-by-contract.csv')


# 3. Display the first five records
print("\nFirst 5 Records:")
print(df.head())

# 4. Display the last five records
print("\nLast 5 Records:")
print(df.tail())

# 5. Check dataset shape
print(f"\nDataset Shape: Rows = {df.shape[0]}, Columns = {df.shape[1]}")

# 6. Display column names
print("\nColumn Names:")
print(df.columns.tolist())


# ------------------------------------------------------------------------------
# PART 2 — DATA EXPLORATION & CLEANING
# ------------------------------------------------------------------------------
print("\n--- PART 2: DATA EXPLORATION & CLEANINGSTARTED ---")

# 7. Check data types
print("\nData Types:")
print(df.dtypes)

# 8. Display statistical information
print("\nStatistical Summary:")
print(df.describe(include='all'))

# 9. Check missing values
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# 10. Check duplicate records
print(f"\nDuplicate Records Count: {df.duplicated().sum()}")

# 11. Remove duplicates if any
df.drop_duplicates(inplace=True)

# 12. Check unique values for each column
print("\nUnique Values Count per Column:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()}")

# 13 & 14. Handle missing values & Convert data types
# Replacing empty spaces in TotalCharges with NaN and converting to float
df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])

# Dropping rows where TotalCharges is missing
df.dropna(subset=['TotalCharges'], inplace=True)

# Standardizing column names to match the assignment PDF requirements
df.rename(columns={
    'customerID': 'Customer_ID', 'gender': 'Gender', 'SeniorCitizen': 'Senior_Citizen',
    'tenure': 'Tenure_Months', 'PhoneService': 'Phone_Service', 'MultipleLines': 'Multiple_Lines',
    'InternetService': 'Internet_Service', 'OnlineSecurity': 'Online_Security', 'OnlineBackup': 'Online_Backup',
    'DeviceProtection': 'Device_Protection', 'TechSupport': 'Tech_Support', 'StreamingTV': 'Streaming_TV',
    'StreamingMovies': 'Streaming_Movies', 'PaperlessBilling': 'Paperless_Billing', 'PaymentMethod': 'Payment_Method',
    'MonthlyCharges': 'Monthly_Charges', 'TotalCharges': 'Total_Charges'
}, inplace=True)

# 15. Create appropriate customer tenure groups
def tenure_group(months):
    if months <= 12: return '0-1 Year'
    elif months <= 24: return '1-2 Years'
    elif months <= 48: return '2-4 Years'
    else: return 'Above 4 Years'

df['Tenure_Group'] = df['Tenure_Months'].apply(tenure_group)

# 16. Verify the cleaned dataset
print("\nCleaned Dataset Info Verification:")
print(df.info())


# ------------------------------------------------------------------------------
# PART 3 — DATA ANALYSIS
# ------------------------------------------------------------------------------
print("\n--- PART 3: DATA ANALYSIS STARTED ---")

# 17. Find total customers
total_cust = df['Customer_ID'].nunique()
print(f"Total Customers: {total_cust}")

# 18. Find total churned customers
total_churned = df[df['Churn'] == 'Yes'].shape[0]
print(f"Total Churned Customers: {total_churned}")

# 19. Find total retained customers
total_retained = df[df['Churn'] == 'No'].shape[0]
print(f"Total Retained Customers: {total_retained}")

# 20. Calculate overall churn rate
churn_rate = (total_churned / total_cust) * 100
print(f"Overall Churn Rate: {churn_rate:.2f}%")

# 21. Calculate average monthly charges
print(f"Average Monthly Charges: {df['Monthly_Charges'].mean():.2f}")

# 22. Calculate average total charges
print(f"Average Total Charges: {df['Total_Charges'].mean():.2f}")

# 23. Calculate average customer tenure
print(f"Average Customer Tenure (Months): {df['Tenure_Months'].mean():.2f}")

# 24. Find customers by gender
print("\nCustomers by Gender:\n", df['Gender'].value_counts())

# 25. Find customers by contract type
print("\nCustomers by Contract Type:\n", df['Contract'].value_counts())

# 26. Find customers by internet service
print("\nCustomers by Internet Service:\n", df['Internet_Service'].value_counts())

# 27. Find customers by payment method
print("\nCustomers by Payment Method:\n", df['Payment_Method'].value_counts())

# 28. Calculate churn rate by gender
print("\nChurn Rate by Gender (%):\n", pd.crosstab(df['Gender'], df['Churn'], normalize='index') * 100)

# 29. Calculate churn rate by contract type
print("\nChurn Rate by Contract Type (%):\n", pd.crosstab(df['Contract'], df['Churn'], normalize='index') * 100)

# 30. Calculate churn rate by internet service
print("\nChurn Rate by Internet Service (%):\n", pd.crosstab(df['Internet_Service'], df['Churn'], normalize='index') * 100)

# 31. Calculate churn rate by payment method
print("\nChurn Rate by Payment Method (%):\n", pd.crosstab(df['Payment_Method'], df['Churn'], normalize='index') * 100)

# 32. Calculate churn rate by senior citizen status
print("\nChurn Rate by Senior Citizen Status (%):\n", pd.crosstab(df['Senior_Citizen'], df['Churn'], normalize='index') * 100)

# 33. Calculate churn rate by tenure group
print("\nChurn Rate by Tenure Group (%):\n", pd.crosstab(df['Tenure_Group'], df['Churn'], normalize='index') * 100)

# 34. Compare monthly charges of churned and retained customers
print("\nAverage Monthly Charges by Churn Status:\n", df.groupby('Churn')['Monthly_Charges'].mean())

# 35. Compare tenure of churned and retained customers
print("\nAverage Tenure (Months) by Churn Status:\n", df.groupby('Churn')['Tenure_Months'].mean())

# 36. Find top 10 customers based on total charges
print("\nTop 10 Customers based on Total Charges:")
print(df.nlargest(10, 'Total_Charges')[['Customer_ID', 'Total_Charges']])


# ------------------------------------------------------------------------------
# SAVE CLEANED FILE FOR POWER BI SUBMISSION
# ------------------------------------------------------------------------------
# Saving the cleaned dataframe to match the requested submission structure
df.to_csv('Customer_Churn_Cleaned.csv', index=False)
print("\nCleaned dataset successfully saved as 'Customer_Churn_Cleaned.csv'!")


# ------------------------------------------------------------------------------
# PART 4 — PYTHON VISUALIZATION
# ------------------------------------------------------------------------------
print("\n--- PART 4: GENERATING PYTHON VISUALIZATIONS ---")

# 1. Churn Distribution — Pie Chart
plt.figure(figsize=(6, 6))
df['Churn'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#66b3ff','#ff9999'], startangle=90)
plt.title('1. Churn Distribution')
plt.ylabel('')
plt.show()

# 2. Customer Distribution by Contract — Bar Chart
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Contract', palette='pastel', hue='Contract', legend=False)
plt.title('2. Customer Distribution by Contract Type')
plt.show()

# 3. Churn by Contract — Bar Chart
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Contract', hue='Churn', palette='Set2')
plt.title('3. Churn by Contract Type')
plt.show()

# 4. Churn by Gender — Bar Chart
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Gender', hue='Churn', palette='muted')
plt.title('4. Churn by Gender')
plt.show()

# 5. Churn by Internet Service — Bar Chart
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Internet_Service', hue='Churn', palette='Set1')
plt.title('5. Churn by Internet Service Type')
plt.show()

# 6. Churn by Payment Method — Bar Chart
plt.figure(figsize=(10, 4))
sns.countplot(data=df, x='Payment_Method', hue='Churn', palette='Dark2')
plt.title('6. Churn by Payment Method')
plt.xticks(rotation=15)
plt.show()

# 7. Tenure Distribution — Histogram
plt.figure(figsize=(7, 4))
sns.histplot(data=df, x='Tenure_Months', kde=True, color='purple', bins=30)
plt.title('7. Customer Tenure Distribution')
plt.show()

# 8. Monthly Charges Distribution — Histogram
plt.figure(figsize=(7, 4))
sns.histplot(data=df, x='Monthly_Charges', kde=True, color='teal', bins=30)
plt.title('8. Monthly Charges Distribution')
plt.show()

# 9. Tenure vs Monthly Charges — Scatter Plot
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Tenure_Months', y='Monthly_Charges', hue='Churn', alpha=0.6)
plt.title('9. Tenure vs Monthly Charges Scatter Plot')
plt.show()

# 10. Monthly Charges by Churn — Box Plot
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x='Churn', y='Monthly_Charges', palette='pastel', hue='Churn', legend=False)
plt.title('10. Monthly Charges by Churn')
plt.show()

# 11. Total Charges by Churn — Box Plot
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x='Churn', y='Total_Charges', palette='coolwarm', hue='Churn', legend=False)
plt.title('11. Total Charges by Churn')
plt.show()

# 12. Churn Rate by Tenure Group — Bar Chart
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Tenure_Group', hue='Churn', order=['0-1 Year', '1-2 Years', '2-4 Years', 'Above 4 Years'])
plt.title('12. Churn Status by Tenure Group')
plt.show()

# 13. Service Usage — Count Plot (Internet Security example)
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='Online_Security', hue='Churn', palette='autumn')
plt.title('13. Churn Status based on Online Security Service')
plt.show()

# 14. Correlation Heatmap
plt.figure(figsize=(8, 5))
