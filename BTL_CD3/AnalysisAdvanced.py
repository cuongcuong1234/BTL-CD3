import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# ================== ADVANCED ANALYSIS & VISUALIZATIONS ==================
print("="*60)
print("ADVANCED ANALYSIS - DETAILED INSIGHTS")
print("="*60)

# Load cleaned data
df = pd.read_csv('data_cleaned.csv')

# ================== 1. CUSTOMER LIFETIME VALUE ANALYSIS ==================
print("\n1. CUSTOMER LIFETIME VALUE (CLV) ANALYSIS")
print("-" * 60)

# Calculate CLV metrics
df['Potential_CLV'] = df['Purchase_Amount'] * df['Frequency_of_Purchase'] * df['Customer_Satisfaction'] / 10

clv_analysis = df.groupby('Customer_Segment').agg({
    'Purchase_Amount': ['mean', 'sum'],
    'Frequency_of_Purchase': 'mean',
    'Customer_Satisfaction': 'mean',
    'Potential_CLV': ['mean', 'sum']
}).round(2)

print("\nCLV by Customer Segment:")
print(clv_analysis)

# Top 20 customers by CLV
top_customers = df.nlargest(20, 'Potential_CLV')[['Customer_ID', 'Age', 'Income_Level', 
                                                     'Purchase_Amount', 'Frequency_of_Purchase',
                                                     'Customer_Satisfaction', 'Potential_CLV']]
print("\nTop 20 Customers by Lifetime Value:")
for idx, row in top_customers.iterrows():
    print(f"  {row['Customer_ID']}: CLV=${row['Potential_CLV']:.2f} | "
          f"Age: {row['Age']} | Income: {row['Income_Level']} | "
          f"Satisfaction: {row['Customer_Satisfaction']}/10")

# ================== 2. CHURN RISK ANALYSIS ==================
print("\n\n2. CHURN RISK ANALYSIS")
print("-" * 60)

# Low satisfaction = high churn risk
churn_threshold = df['Customer_Satisfaction'].quantile(0.33)
df['Churn_Risk'] = df['Customer_Satisfaction'] <= churn_threshold

churn_stats = df['Churn_Risk'].value_counts()
print(f"\nCustomers by Churn Risk:")
print(f"  High Risk (Satisfaction <= {churn_threshold:.1f}): {churn_stats[True]} customers")
print(f"  Low Risk (Satisfaction > {churn_threshold:.1f}): {churn_stats[False]} customers")

# High-risk segments
high_risk = df[df['Churn_Risk']]
print(f"\nHigh-Risk Customer Profile:")
print(f"  - Average Age: {high_risk['Age'].mean():.1f}")
print(f"  - Average Spending: ${high_risk['Purchase_Amount'].mean():.2f}")
print(f"  - Average Satisfaction: {high_risk['Customer_Satisfaction'].mean():.2f}/10")
print(f"  - Top Income Level: {high_risk['Income_Level'].mode()[0]}")
print(f"  - Top Location: {high_risk['Location'].mode()[0]}")

# ================== 3. CHANNEL PERFORMANCE ==================
print("\n\n3. PURCHASE CHANNEL PERFORMANCE")
print("-" * 60)

channel_analysis = df.groupby('Purchase_Channel').agg({
    'Purchase_Amount': ['mean', 'sum', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean',
    'Brand_Loyalty': 'mean'
}).round(2)

channel_analysis.columns = ['Avg_Purchase', 'Total_Revenue', 'Transaction_Count', 
                            'Satisfaction', 'Return_Rate', 'Brand_Loyalty']
print("\nChannel Performance Metrics:")
print(channel_analysis.sort_values('Total_Revenue', ascending=False))

# ================== 4. SEASONAL & TIME ANALYSIS ==================
print("\n\n4. PURCHASE TIMING ANALYSIS")
print("-" * 60)

time_analysis = df.groupby('Time_of_Purchase').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)

time_analysis.columns = ['Avg_Purchase', 'Transaction_Count', 'Satisfaction']
print("\nPurchase Timing Distribution:")
print(time_analysis.sort_values('Transaction_Count', ascending=False))

# ================== 5. DEVICE & PLATFORM ANALYSIS ==================
print("\n\n5. DEVICE & PLATFORM ANALYSIS")
print("-" * 60)

device_analysis = df.groupby('Device_Used_for_Shopping').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean'
}).round(2)

device_analysis.columns = ['Avg_Purchase', 'Transaction_Count', 'Satisfaction', 'Frequency']
print("\nDevice Performance:")
print(device_analysis.sort_values('Transaction_Count', ascending=False))

# ================== 6. LOYALTY PROGRAM IMPACT ==================
print("\n\n6. LOYALTY PROGRAM EFFECTIVENESS")
print("-" * 60)

loyalty_comparison = df.groupby('Customer_Loyalty_Program_Member').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean',
    'Brand_Loyalty': 'mean',
    'Return_Rate': 'mean'
}).round(2)

loyalty_comparison.columns = ['Avg_Purchase', 'Count', 'Satisfaction', 'Frequency', 'Brand_Loyalty', 'Return_Rate']
loyalty_comparison.index = ['Non-Member', 'Member']

print("\nLoyalty Program Impact:")
print(loyalty_comparison)

member_uplift = ((loyalty_comparison.loc['Member', 'Avg_Purchase'] - 
                 loyalty_comparison.loc['Non-Member', 'Avg_Purchase']) / 
                loyalty_comparison.loc['Non-Member', 'Avg_Purchase'] * 100)
print(f"\nSpending Uplift from Loyalty Program: {member_uplift:+.1f}%")

# ================== 7. DISCOUNT STRATEGY ANALYSIS ==================
print("\n\n7. DISCOUNT STRATEGY EFFECTIVENESS")
print("-" * 60)

discount_analysis = df.groupby('Discount_Used').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean'
}).round(2)

discount_analysis.columns = ['Avg_Purchase', 'Count', 'Satisfaction', 'Return_Rate']
discount_analysis.index = ['No Discount', 'With Discount']

print("\nDiscount Impact Analysis:")
print(discount_analysis)

# ================== 8. BRAND LOYALTY PATTERNS ==================
print("\n\n8. BRAND LOYALTY ANALYSIS")
print("-" * 60)

loyalty_segments = pd.cut(df['Brand_Loyalty'], bins=[0, 2, 4, 6, 10], 
                         labels=['Very Low', 'Low', 'Medium', 'High'])
df['Loyalty_Segment'] = loyalty_segments

loyalty_profile = df.groupby('Loyalty_Segment').agg({
    'Purchase_Amount': 'mean',
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean',
    'Return_Rate': 'mean'
}).round(2)

print("\nBrand Loyalty Profiles:")
print(loyalty_profile)

print(f"\nBrand Loyalty Distribution:")
print(loyalty_segments.value_counts())

# ================== 9. PAYMENT METHOD PREFERENCES ==================
print("\n\n9. PAYMENT METHOD PREFERENCES")
print("-" * 60)

payment_analysis = df.groupby('Payment_Method').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)

payment_analysis.columns = ['Avg_Purchase', 'Count', 'Satisfaction']
print("\nPayment Method Statistics:")
print(payment_analysis.sort_values('Count', ascending=False))

# ================== 10. COMPREHENSIVE VISUALIZATIONS ==================
print("\n\n" + "="*60)
print("GENERATING ADVANCED VISUALIZATIONS")
print("="*60)

fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle('Advanced E-Commerce Consumer Behavior Analytics', 
             fontsize=20, fontweight='bold', y=0.995)

# 1. Customer Lifetime Value Distribution
axes[0, 0].hist(df['Potential_CLV'], bins=30, color='darkgreen', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Lifetime Value ($)')
axes[0, 0].set_ylabel('Number of Customers')
axes[0, 0].set_title('Customer Lifetime Value Distribution')
axes[0, 0].axvline(df['Potential_CLV'].mean(), color='red', linestyle='--', 
                   label=f'Mean: ${df["Potential_CLV"].mean():.2f}')
axes[0, 0].legend()

# 2. Churn Risk Segment
churn_colors = ['#2ecc71', '#e74c3c']
churn_counts = df['Churn_Risk'].value_counts()
axes[0, 1].bar(['Low Risk', 'High Risk'], [churn_counts[False], churn_counts[True]], 
              color=churn_colors, edgecolor='black', alpha=0.7)
axes[0, 1].set_ylabel('Number of Customers')
axes[0, 1].set_title('Churn Risk Segmentation')
for i, v in enumerate([churn_counts[False], churn_counts[True]]):
    axes[0, 1].text(i, v + 10, str(v), ha='center', fontweight='bold')

# 3. Channel Performance
channel_revenue = df.groupby('Purchase_Channel')['Purchase_Amount'].sum().sort_values(ascending=False)
axes[0, 2].barh(range(len(channel_revenue)), channel_revenue.values, color='steelblue', edgecolor='black')
axes[0, 2].set_yticks(range(len(channel_revenue)))
axes[0, 2].set_yticklabels(channel_revenue.index)
axes[0, 2].set_xlabel('Total Revenue ($)')
axes[0, 2].set_title('Revenue by Purchase Channel')
axes[0, 2].invert_yaxis()

# 4. Time of Purchase Distribution
time_counts = df['Time_of_Purchase'].value_counts()
colors_time = plt.cm.Set3(np.linspace(0, 1, len(time_counts)))
axes[1, 0].pie(time_counts.values, labels=time_counts.index, autopct='%1.1f%%', 
              startangle=90, colors=colors_time)
axes[1, 0].set_title('Purchases by Time of Day')

# 5. Device Usage
device_usage = df['Device_Used_for_Shopping'].value_counts()
axes[1, 1].bar(range(len(device_usage)), device_usage.values, color='coral', edgecolor='black', alpha=0.7)
axes[1, 1].set_xticks(range(len(device_usage)))
axes[1, 1].set_xticklabels(device_usage.index, rotation=45, ha='right')
axes[1, 1].set_ylabel('Number of Purchases')
axes[1, 1].set_title('Device Usage Distribution')

# 6. Loyalty Program Impact
loyalty_data = pd.DataFrame({
    'Non-Member': loyalty_comparison.loc['Non-Member'],
    'Member': loyalty_comparison.loc['Member']
})
x = np.arange(len(loyalty_data.columns))
width = 0.35
metrics = loyalty_data.index[:3]
for i, metric in enumerate(metrics):
    axes[1, 2].bar(x + i*width/3, loyalty_data.loc[metric], width/3, label=metric)
axes[1, 2].set_ylabel('Value')
axes[1, 2].set_title('Loyalty Program Impact')
axes[1, 2].set_xticks(x + width/3)
axes[1, 2].set_xticklabels(loyalty_data.columns)
axes[1, 2].legend()

# 7. Discount Sensitivity
discount_data = df['Discount_Used'].value_counts()
colors_disc = ['#FF9999', '#66B2FF']
axes[2, 0].bar(['No Discount', 'With Discount'], 
              [discount_data[False], discount_data[True]], 
              color=colors_disc, edgecolor='black', alpha=0.7)
axes[2, 0].set_ylabel('Number of Purchases')
axes[2, 0].set_title('Discount Usage Pattern')

# 8. Brand Loyalty Segments
brand_loyal = df['Loyalty_Segment'].value_counts()
axes[2, 1].barh(range(len(brand_loyal)), brand_loyal.values, color='mediumpurple', edgecolor='black')
axes[2, 1].set_yticks(range(len(brand_loyal)))
axes[2, 1].set_yticklabels(brand_loyal.index)
axes[2, 1].set_xlabel('Number of Customers')
axes[2, 1].set_title('Brand Loyalty Segments')
axes[2, 1].invert_yaxis()

# 9. Return Rate vs Satisfaction
scatter = axes[2, 2].scatter(df['Return_Rate'], df['Customer_Satisfaction'], 
                            c=df['Purchase_Amount'], cmap='plasma', alpha=0.6, s=50)
axes[2, 2].set_xlabel('Return Rate (%)')
axes[2, 2].set_ylabel('Customer Satisfaction')
axes[2, 2].set_title('Returns vs Satisfaction (colored by Amount)')
cbar = plt.colorbar(scatter, ax=axes[2, 2])
cbar.set_label('Purchase Amount ($)')

plt.tight_layout()
plt.savefig('advanced_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Advanced visualization saved as 'advanced_analysis.png'")
plt.close()

# ================== 11. SAVE DETAILED REPORTS ==================
print("\nSaving detailed analysis reports...")

# Save churn analysis
churn_report = df[df['Churn_Risk']][['Customer_ID', 'Age', 'Income_Level', 'Purchase_Amount',
                                       'Customer_Satisfaction', 'Location']]
churn_report.to_csv('high_churn_risk_customers.csv', index=False)
print("✓ Churn risk analysis saved")

# Save CLV analysis
clv_report = df[['Customer_ID', 'Age', 'Income_Level', 'Purchase_Amount',
                 'Frequency_of_Purchase', 'Customer_Satisfaction', 'Potential_CLV']].sort_values('Potential_CLV', ascending=False)
clv_report.to_csv('customer_lifetime_value.csv', index=False)
print("✓ CLV analysis saved")

# Save channel performance
df.groupby('Purchase_Channel').agg({
    'Purchase_Amount': ['mean', 'sum', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean'
}).to_csv('channel_performance.csv')
print("✓ Channel performance saved")

# Save device analysis
df.groupby('Device_Used_for_Shopping').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).to_csv('device_analysis.csv')
print("✓ Device analysis saved")

print("\n" + "="*60)
print("ADVANCED ANALYSIS COMPLETE!")
print("="*60)
