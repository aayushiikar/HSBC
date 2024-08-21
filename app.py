import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define URL for the dataset
file_path = 'C:/Users/aayus/OneDrive/Desktop/mom/cleaned_data.csv'

# Load the dataset with caching
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Load data
df = load_data(file_path)

# Display encoding information
st.write("## Dataset Encoding Information")

# Gender Mapping Table
st.write("### Gender Mapping Table")
gender_mapping_df = pd.DataFrame({
    'Original Gender': ['E', 'F', 'M', 'U'],
    'Encoded Value': [1, 2, 3, 4]
})
st.dataframe(gender_mapping_df)

# Category Mapping Table
st.write("### Category Mapping Table")
category_mapping_df = pd.DataFrame({
    'Original Category': [
        'es_barsandrestaurants', 'es_contents', 'es_fashion', 'es_food',
        'es_health', 'es_home', 'es_hotelservices', 'es_hyper', 'es_leisure',
        'es_otherservices', 'es_sportsandtoys', 'es_tech', 'es_transportation',
        'es_travel', 'es_wellnessandbeauty'
    ],
    'Encoded Value': list(range(15))
})
st.dataframe(category_mapping_df)

# Display the data
st.write("## Dataset Overview")
st.dataframe(df.head())

# Data Insights
st.write("## Data Insights")

# Filter out the fraudulent transactions
fraud_df = df[df['fraud'] == 1]

# Gender Distribution
st.write("### Fraudulent Transactions by Gender")
gender_mapping = {1: 'LGBTQ', 2: 'Female', 3: 'Male', 4: 'Unspecified'}
fraud_df['gender_label'] = fraud_df['gender'].map(gender_mapping)
gender_counts = fraud_df['gender_label'].value_counts()

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], startangle=140)
ax.set_title('Fraudulent Transactions by Gender')
st.pyplot(fig)

# Amount Range Distribution
st.write("### Histogram of Fraudulent Transactions by Amount Range")
bins = [0, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
labels = ['0-50', '50-100', '100-200', '200-500', '500-1000', '1000-2000', '2000-5000', '5000-10000', '10000-20000', '20000-50000', '50000-100000']
fraud_df['amount_range'] = pd.cut(fraud_df['amount'], bins=bins, labels=labels, right=False)

fig, ax = plt.subplots(figsize=(12, 6))
fraud_df['amount_range'].value_counts().sort_index().plot(kind='bar', color='orange', ax=ax)
ax.set_title('Histogram of Fraudulent Transactions by Amount Range')
ax.set_xlabel('Amount Range')
ax.set_ylabel('Number of Fraudulent Transactions')
ax.grid(axis='y')
st.pyplot(fig)

# Fraudulent Transactions by Category
st.write("### Fraudulent Transactions by Category")
category_mapping = {
    0: 'es_barsandrestaurants',
    1: 'es_contents',
    2: 'es_fashion',
    3: 'es_food',
    4: 'es_health',
    5: 'es_home',
    6: 'es_hotelservices',
    7: 'es_hyper',
    8: 'es_leisure',
    9: 'es_otherservices',
    10: 'es_sportsandtoys',
    11: 'es_tech',
    12: 'es_transportation',
    13: 'es_travel',
    14: 'es_wellnessandbeauty'
}
df['category'] = df['category'].map(category_mapping)
category_fraud = df[df['fraud'] == 1]['category'].value_counts()
category_total = df['category'].value_counts()

category_stats = pd.DataFrame({
    'Fraudulent Transactions': category_fraud,
    'Total Transactions': category_total
}).fillna(0)

category_stats['Fraud Rate'] = category_stats['Fraudulent Transactions'] / category_stats['Total Transactions'] * 100

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=category_stats.index, y=category_stats['Fraudulent Transactions'], palette='viridis', ax=ax)
ax.set_title('Number of Fraudulent Transactions by Category')
ax.set_xlabel('Category')
ax.set_ylabel('Number of Fraudulent Transactions')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=category_stats.index, y=category_stats['Total Transactions'], palette='viridis', ax=ax)
ax.set_title('Total Number of Transactions by Category')
ax.set_xlabel('Category')
ax.set_ylabel('Total Number of Transactions')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig)

# Rerun Button
if st.button("Rerun"):
    st.experimental_rerun()
