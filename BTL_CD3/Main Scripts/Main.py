import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from itertools import combinations
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ================== 1. LOAD & CLEAN DATA ==================
print("="*60)
print("1. LOADING AND CLEANING DATA")
print("="*60)

df = pd.read_csv('Ecommerce_Consumer_Behavior_Analysis_Data.csv')
print(f"Original data shape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# Make a copy for processing
df_clean = df.copy()

# Clean Purchase_Amount: Remove "$" and convert to float
df_clean['Purchase_Amount'] = df_clean['Purchase_Amount'].str.replace('$', '').astype(float)

# Handle missing values
# For Social_Media_Influence and Engagement_with_Ads, fill with mode
df_clean['Social_Media_Influence'].fillna(df_clean['Social_Media_Influence'].mode()[0], inplace=True)
df_clean['Engagement_with_Ads'].fillna(df_clean['Engagement_with_Ads'].mode()[0], inplace=True)

# Remove duplicates if any
initial_rows = len(df_clean)
df_clean.drop_duplicates(inplace=True)
print(f"\nRemoved {initial_rows - len(df_clean)} duplicate rows")

# Validate data types
print(f"\nCleaned data shape: {df_clean.shape}")
print(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
print("✓ Data cleaning completed successfully!")

# ================== 2. EXPLORATORY DATA ANALYSIS ==================
print("\n" + "="*60)
print("2. EXPLORATORY DATA ANALYSIS")
print("="*60)

print(f"\nBasic Statistics:")
print(f"  - Average Purchase Amount: ${df_clean['Purchase_Amount'].mean():.2f}")
print(f"  - Median Purchase Amount: ${df_clean['Purchase_Amount'].median():.2f}")
print(f"  - Min Purchase Amount: ${df_clean['Purchase_Amount'].min():.2f}")
print(f"  - Max Purchase Amount: ${df_clean['Purchase_Amount'].max():.2f}")
print(f"\n  - Average Customer Age: {df_clean['Age'].mean():.1f} years")
print(f"  - Average Customer Satisfaction: {df_clean['Customer_Satisfaction'].mean():.2f}/10")

print(f"\nTop Purchase Categories:")
print(df_clean['Purchase_Category'].value_counts().head(10))

print(f"\nIncome Level Distribution:")
print(df_clean['Income_Level'].value_counts())

# ================== 3. PRODUCTS FREQUENTLY BOUGHT TOGETHER ==================
print("\n" + "="*60)
print("3. MARKET BASKET ANALYSIS - PRODUCTS BOUGHT TOGETHER")
print("="*60)

# Group by customer to find what products each customer bought
customer_products = df_clean.groupby('Customer_ID')['Purchase_Category'].apply(list).values

# Find product pairs
product_pairs = []
product_counts = Counter()

for products in customer_products:
    unique_products = list(set(products))
    product_counts.update(unique_products)
    if len(unique_products) > 1:
        pairs = list(combinations(sorted(unique_products), 2))
        product_pairs.extend(pairs)

# Count pair frequencies
pair_counts = Counter(product_pairs)

print(f"\nTop 15 Product Combinations Bought Together:")
for idx, (pair, count) in enumerate(pair_counts.most_common(15), 1):
    product1, product2 = pair
    print(f"  {idx}. {product1} + {product2}: {count} times")

# Top individual products
print(f"\nTop 10 Most Purchased Categories:")
for idx, (product, count) in enumerate(product_counts.most_common(10), 1):
    percentage = (count / sum(product_counts.values())) * 100
    print(f"  {idx}. {product}: {count} purchases ({percentage:.1f}%)")

# ================== 4. CUSTOMER SEGMENTATION & SPENDING ANALYSIS ==================
print("\n" + "="*60)
print("4. CUSTOMER SEGMENTATION & SPENDING ANALYSIS")
print("="*60)

# Prepare features for segmentation
segmentation_features = ['Age', 'Purchase_Amount', 'Frequency_of_Purchase', 
                         'Customer_Satisfaction', 'Brand_Loyalty']

X_segment = df_clean[segmentation_features].copy()
scaler = StandardScaler()
X_segment_scaled = scaler.fit_transform(X_segment)

# K-means clustering (4 segments)
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df_clean['Customer_Segment'] = kmeans.fit_predict(X_segment_scaled)

# Analyze segments
print(f"\nCustomer Segments (n={n_clusters}):")
for segment in range(n_clusters):
    segment_data = df_clean[df_clean['Customer_Segment'] == segment]
    print(f"\n  Segment {segment} ({len(segment_data)} customers):")
    print(f"    - Avg Age: {segment_data['Age'].mean():.1f}")
    print(f"    - Avg Spending: ${segment_data['Purchase_Amount'].mean():.2f}")
    print(f"    - Avg Purchase Frequency: {segment_data['Frequency_of_Purchase'].mean():.1f}")
    print(f"    - Avg Satisfaction: {segment_data['Customer_Satisfaction'].mean():.2f}/10")
    print(f"    - Avg Brand Loyalty: {segment_data['Brand_Loyalty'].mean():.2f}")

# Spending by Income Level
print(f"\nSpending Analysis by Income Level:")
income_spending = df_clean.groupby('Income_Level').agg({
    'Purchase_Amount': ['mean', 'median', 'sum', 'count']
}).round(2)
income_spending.columns = ['Mean', 'Median', 'Total', 'Count']
print(income_spending.sort_values('Mean', ascending=False))

# Spending by Gender
print(f"\nSpending Analysis by Gender:")
gender_spending = df_clean.groupby('Gender').agg({
    'Purchase_Amount': ['mean', 'median', 'sum', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)
gender_spending.columns = ['Avg_Amount', 'Median_Amount', 'Total_Amount', 'Count', 'Satisfaction']
print(gender_spending)

# ================== 5. DATA VISUALIZATION ==================
print("\n" + "="*60)
print("5. CREATING VISUALIZATIONS")
print("="*60)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 12)

fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle('E-Commerce Consumer Behavior Analysis', fontsize=20, fontweight='bold', y=0.995)

# 1. Purchase Amount Distribution
axes[0, 0].hist(df_clean['Purchase_Amount'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Purchase Amount ($)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Distribution of Purchase Amounts')
axes[0, 0].axvline(df_clean['Purchase_Amount'].mean(), color='red', linestyle='--', label=f'Mean: ${df_clean["Purchase_Amount"].mean():.2f}')
axes[0, 0].legend()

# 2. Top 10 Purchase Categories
top_categories = df_clean['Purchase_Category'].value_counts().head(10)
axes[0, 1].barh(range(len(top_categories)), top_categories.values, color='coral')
axes[0, 1].set_yticks(range(len(top_categories)))
axes[0, 1].set_yticklabels(top_categories.index)
axes[0, 1].set_xlabel('Number of Purchases')
axes[0, 1].set_title('Top 10 Product Categories')
axes[0, 1].invert_yaxis()

# 3. Spending by Income Level
income_order = ['Low', 'Medium', 'High']
income_data = df_clean[df_clean['Income_Level'].isin(income_order)].copy()
sns.boxplot(x='Income_Level', y='Purchase_Amount', data=income_data, order=income_order, ax=axes[0, 2], palette='Set2')
axes[0, 2].set_ylabel('Purchase Amount ($)')
axes[0, 2].set_xlabel('Income Level')
axes[0, 2].set_title('Spending by Income Level')

# 4. Customer Age Distribution
axes[1, 0].hist(df_clean['Age'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('Age (years)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('Customer Age Distribution')

# 5. Customer Satisfaction vs Purchase Amount
scatter = axes[1, 1].scatter(df_clean['Purchase_Amount'], df_clean['Customer_Satisfaction'], 
                             c=df_clean['Age'], cmap='viridis', alpha=0.6, s=50)
axes[1, 1].set_xlabel('Purchase Amount ($)')
axes[1, 1].set_ylabel('Customer Satisfaction')
axes[1, 1].set_title('Satisfaction vs Spending (colored by Age)')
cbar = plt.colorbar(scatter, ax=axes[1, 1])
cbar.set_label('Age')

# 6. Spending by Gender
gender_avg = df_clean.groupby('Gender')['Purchase_Amount'].mean()
colors = ['#FF69B4', '#4169E1']
axes[1, 2].bar(gender_avg.index, gender_avg.values, color=colors, alpha=0.7, edgecolor='black')
axes[1, 2].set_ylabel('Average Purchase Amount ($)')
axes[1, 2].set_title('Average Spending by Gender')
for i, v in enumerate(gender_avg.values):
    axes[1, 2].text(i, v + 5, f'${v:.2f}', ha='center', fontweight='bold')

# 7. Purchase Frequency Distribution
axes[2, 0].hist(df_clean['Frequency_of_Purchase'], bins=15, color='purple', edgecolor='black', alpha=0.7)
axes[2, 0].set_xlabel('Purchase Frequency')
axes[2, 0].set_ylabel('Number of Customers')
axes[2, 0].set_title('Customer Purchase Frequency Distribution')

# 8. Customer Segments (3D representation on 2D)
segment_spending = df_clean.groupby('Customer_Segment')['Purchase_Amount'].mean()
segment_size = df_clean['Customer_Segment'].value_counts().sort_index()
colors_segment = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
axes[2, 1].scatter(segment_size.values, segment_spending.values, 
                   s=[x*10 for x in segment_size.values], 
                   c=colors_segment, alpha=0.6, edgecolors='black', linewidth=2)
for i, segment in enumerate(range(n_clusters)):
    axes[2, 1].annotate(f'Segment {segment}', 
                       (segment_size[segment], segment_spending[segment]),
                       xytext=(5, 5), textcoords='offset points', fontweight='bold')
axes[2, 1].set_xlabel('Number of Customers')
axes[2, 1].set_ylabel('Average Spending ($)')
axes[2, 1].set_title('Customer Segments Overview')

# 9. Payment Methods
payment_counts = df_clean['Payment_Method'].value_counts()
axes[2, 2].pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%', startangle=90)
axes[2, 2].set_title('Payment Method Distribution')

plt.tight_layout()
plt.savefig('consumer_behavior_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved as 'consumer_behavior_analysis.png'")
plt.close()

# ================== 6. PREDICTIVE MODEL - SPENDING PREDICTION ==================
print("\n" + "="*60)
print("6. PREDICTIVE MODEL - CUSTOMER SPENDING PREDICTION")
print("="*60)

# Prepare features for prediction
# Encode categorical variables
le_dict = {}
categorical_features = ['Gender', 'Income_Level', 'Marital_Status', 'Education_Level', 
                       'Occupation', 'Location', 'Purchase_Channel', 'Social_Media_Influence',
                       'Discount_Sensitivity', 'Device_Used_for_Shopping', 'Payment_Method',
                       'Time_of_Purchase', 'Purchase_Intent', 'Shipping_Preference']

df_model = df_clean.copy()

for feature in categorical_features:
    le = LabelEncoder()
    df_model[feature] = le.fit_transform(df_model[feature])
    le_dict[feature] = le

# Select features for the model
feature_columns = ['Age', 'Frequency_of_Purchase', 'Brand_Loyalty', 'Product_Rating',
                  'Time_Spent_on_Product_Research(hours)', 'Return_Rate',
                  'Customer_Satisfaction', 'Time_to_Decision'] + categorical_features

X = df_model[feature_columns]
y = df_model['Purchase_Amount']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("\nTraining Random Forest model...")
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15)
model.fit(X_train, y_train)

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Evaluation Metrics
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)

print(f"\nModel Performance:")
print(f"  Train RMSE: ${train_rmse:.2f}")
print(f"  Test RMSE: ${test_rmse:.2f}")
print(f"  Train MAE: ${train_mae:.2f}")
print(f"  Test MAE: ${test_mae:.2f}")
print(f"  Train R²: {train_r2:.4f}")
print(f"  Test R²: {test_r2:.4f}")

# Feature Importance
feature_importance = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\nTop 15 Most Important Features:")
for idx, row in feature_importance.head(15).iterrows():
    print(f"  {row['Feature']}: {row['Importance']:.4f}")

# ================== 7. PREDICTION EXAMPLES ==================
print("\n" + "="*60)
print("7. PREDICTION EXAMPLES - SAMPLE CUSTOMER SPENDING")
print("="*60)

# Create sample predictions
sample_indices = np.random.choice(X_test.index, 5, replace=False)
sample_X = X_test.loc[sample_indices]
sample_y_actual = y_test.loc[sample_indices]
sample_y_pred = model.predict(sample_X)

print("\nSample Predictions (vs Actual Spending):")
for i, (idx, pred, actual) in enumerate(zip(sample_indices, sample_y_pred, sample_y_actual), 1):
    error = abs(pred - actual) / actual * 100
    print(f"  Customer {i}:")
    print(f"    Predicted Spending: ${pred:.2f}")
    print(f"    Actual Spending: ${actual:.2f}")
    print(f"    Error: {error:.1f}%\n")

# ================== 8. SAVE RESULTS ==================
print("="*60)
print("8. SAVING RESULTS")
print("="*60)

# Save cleaned data
df_clean.to_csv('data_cleaned.csv', index=False)
print("✓ Cleaned data saved as 'data_cleaned.csv'")

# Save customer segments
segments_summary = df_clean.groupby('Customer_Segment').agg({
    'Purchase_Amount': ['mean', 'median', 'count'],
    'Age': 'mean',
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean'
}).round(2)
segments_summary.to_csv('customer_segments_analysis.csv')
print("✓ Customer segments analysis saved as 'customer_segments_analysis.csv'")

# Save top product combinations
pairs_df = pd.DataFrame(list(pair_counts.most_common(50)), 
                        columns=['Product_Combination', 'Count'])
pairs_df['Pair_1'] = pairs_df['Product_Combination'].str[0]
pairs_df['Pair_2'] = pairs_df['Product_Combination'].str[1]
pairs_df = pairs_df[['Pair_1', 'Pair_2', 'Count']]
pairs_df.to_csv('product_combinations.csv', index=False)
print("✓ Product combinations saved as 'product_combinations.csv'")

# Save feature importance
feature_importance.to_csv('feature_importance.csv', index=False)
print("✓ Feature importance saved as 'feature_importance.csv'")

# Save model predictions
prediction_results = pd.DataFrame({
    'Actual_Spending': y_test.values,
    'Predicted_Spending': y_pred_test,
    'Prediction_Error': np.abs(y_test.values - y_pred_test),
    'Error_Percentage': (np.abs(y_test.values - y_pred_test) / y_test.values * 100)
})
prediction_results.to_csv('model_predictions.csv', index=False)
print("✓ Model predictions saved as 'model_predictions.csv'")

# ================== SUMMARY ==================
print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)
print(f"\n✓ Generated outputs:")
print(f"  1. consumer_behavior_analysis.png - 9-panel visualization")
print(f"  2. data_cleaned.csv - Cleaned transaction data")
print(f"  3. customer_segments_analysis.csv - Customer segmentation insights")
print(f"  4. product_combinations.csv - Top product pairs")
print(f"  5. feature_importance.csv - Predictive model feature importance")
print(f"  6. model_predictions.csv - Customer spending predictions")
print(f"\n✓ Analysis Summary:")
print(f"  - Analyzed {len(df_clean)} transactions")
print(f"  - {df_clean['Purchase_Category'].nunique()} product categories")
print(f"  - {n_clusters} customer segments identified")
print(f"  - Model achieved {test_r2:.2%} accuracy on test set")
print("="*60)
