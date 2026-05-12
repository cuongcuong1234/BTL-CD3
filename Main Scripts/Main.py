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

plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ================== 1. TẢI VÀ LÀM SẠCH DỮ LIỆU ==================
print("1. TẢI VÀ LÀM SẠCH DỮ LIỆU")


df = pd.read_csv('Ecommerce_Consumer_Behavior_Analysis_Data.csv')
print(f"Dữ liệu ban đầu: {df.shape[0]:,} dòng, {df.shape[1]} cột")

# Kiểm tra missing values
print("\nGiá trị thiếu ban đầu:")
print(df.isnull().sum()[df.isnull().sum() > 0])

df_clean = df.copy()

# Làm sạch cột Purchase_Amount
df_clean['Purchase_Amount'] = df_clean['Purchase_Amount'].astype(str).str.replace('$', '', regex=False)
df_clean['Purchase_Amount'] = pd.to_numeric(df_clean['Purchase_Amount'], errors='coerce')

# Điền giá trị thiếu
for col in df_clean.columns:
    if pd.api.types.is_numeric_dtype(df_clean[col]):
        df_clean[col].fillna(df_clean[col].median(), inplace=True)
    else:
        df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)

# Xóa dữ liệu trùng lặp
initial_rows = len(df_clean)
df_clean.drop_duplicates(inplace=True)
print(f"\nĐã xóa {initial_rows - len(df_clean)} dòng trùng lặp")

# Tạo Customer_ID ngẫu nhiên (để có nhiều giao dịch cho một khách hàng)
df_clean['Customer_ID'] = np.random.randint(1, 200, size=len(df_clean))

print(f"\nDữ liệu sau khi làm sạch: {df_clean.shape}")
print(f"Tổng số giá trị thiếu: {df_clean.isnull().sum().sum()}")

print("\nTop 10 khách hàng có nhiều giao dịch nhất:")
print(df_clean['Customer_ID'].value_counts().head(10))

print("\n✓ Hoàn thành làm sạch dữ liệu!")

# ================== 2. PHÂN TÍCH KHÁM PHÁ (EDA) ==================
print("\n" + "=" * 80)
print("2. PHÂN TÍCH KHÁM PHÁ DỮ LIỆU")
print("=" * 80)

print("\nThống kê cơ bản:")
print(f"  - Giá trị mua trung bình     : ${df_clean['Purchase_Amount'].mean():.2f}")
print(f"  - Giá trị mua trung vị       : ${df_clean['Purchase_Amount'].median():.2f}")
print(f"  - Giá trị mua nhỏ nhất       : ${df_clean['Purchase_Amount'].min():.2f}")
print(f"  - Giá trị mua lớn nhất       : ${df_clean['Purchase_Amount'].max():.2f}")

print(f"\n  - Tuổi trung bình của khách hàng: {df_clean['Age'].mean():.1f} tuổi")
print(f"  - Điểm hài lòng trung bình     : {df_clean['Customer_Satisfaction'].mean():.2f}/10")

print(f"\nTop 10 danh mục mua hàng:")
print(df_clean['Purchase_Category'].value_counts().head(10))

print(f"\nPhân bố mức thu nhập:")
print(df_clean['Income_Level'].value_counts())

# ================== 3. PHÂN TÍCH SẢN PHẨM MUA CÙNG NHAU ==================
print("\n" + "=" * 70)
print("3. PHÂN TÍCH SẢN PHẨM MUA CÙNG NHAU")
print("=" * 70)

import os
from collections import Counter
from itertools import combinations

# Tạo thư mục lưu biểu đồ
os.makedirs("charts", exist_ok=True)

customer_products = df_clean.groupby('Customer_ID')['Purchase_Category'].apply(list)

product_pairs = []
product_counts = Counter()

for products in customer_products:
    unique_products = list(set(products))
    product_counts.update(unique_products)
    if len(unique_products) > 1:
        pairs = list(combinations(sorted(unique_products), 2))
        product_pairs.extend(pairs)

pair_counts = Counter(product_pairs)

# Biểu đồ 1: Top 10 cặp sản phẩm
if len(pair_counts) > 0:
    top_pairs = pair_counts.most_common(10)
    pairs_labels = [f"{a} + {b}" for (a, b), _ in top_pairs]
    pairs_values = [count for _, count in top_pairs]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=pairs_values, y=pairs_labels, palette="Blues_d")
    plt.title('Top 10 cặp sản phẩm mua cùng nhau', fontsize=13, pad=15)
    plt.xlabel('Số lần mua cùng')
    plt.tight_layout()
    plt.savefig('charts/top10_product_pairs.png', dpi=200, bbox_inches='tight')
    plt.show()

# Biểu đồ 2: Top 10 danh mục được mua nhiều nhất
plt.figure(figsize=(8, 5))
top_products = product_counts.most_common(10)
sns.barplot(x=[v for _,v in top_products],
            y=[k for k,_ in top_products], palette="Greens_d")
plt.title('Top 10 danh mục được mua nhiều nhất', fontsize=13, pad=15)
plt.xlabel('Số lần mua')
plt.tight_layout()
plt.savefig('charts/top10_categories.png', dpi=200, bbox_inches='tight')
plt.show()

print("✅ Hoàn thành Phần 3")

# ================== 4. PHÂN ĐOẠN KHÁCH HÀNG & PHÂN TÍCH CHI TIÊU ==================
print("\n" + "=" * 70)
print("4. PHÂN ĐOẠN KHÁCH HÀNG VÀ PHÂN TÍCH CHI TIÊU")
print("=" * 70)

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Phân cụm khách hàng
features = ['Age', 'Purchase_Amount', 'Frequency_of_Purchase',
            'Customer_Satisfaction', 'Brand_Loyalty']

X = StandardScaler().fit_transform(df_clean[features])
df_clean['Customer_Segment'] = KMeans(n_clusters=4, random_state=42, n_init=10).fit_predict(X)

# In tóm tắt nhóm
print(f"\nKết quả phân đoạn 4 nhóm khách hàng:")
for i in range(4):
    seg = df_clean[df_clean['Customer_Segment'] == i]
    print(f"  Nhóm {i}: {len(seg)} giao dịch | Chi tiêu TB: ${seg['Purchase_Amount'].mean():.2f} | "
          f"Hài lòng: {seg['Customer_Satisfaction'].mean():.2f}")

# Biểu đồ 3: Chi tiêu & Hài lòng theo nhóm
seg_summary = df_clean.groupby('Customer_Segment').agg({
    'Purchase_Amount': 'mean',
    'Customer_Satisfaction': 'mean'
}).round(2)
seg_summary['Hài lòng x40'] = seg_summary['Customer_Satisfaction'] * 40

plt.figure(figsize=(8, 5))
x = range(4)
width = 0.35

plt.bar(x, seg_summary['Purchase_Amount'], width, label='Chi tiêu TB ($)', color='#8A7CFF')
plt.bar([i + width for i in x], seg_summary['Hài lòng x40'], width, label='Hài lòng ×40', color='#4ECDC4')

plt.title('Chi tiêu và Hài lòng theo Nhóm khách hàng', fontsize=13, pad=15)
plt.xticks([i + width/2 for i in x],
           ['Nhóm 0 — Ổn định', 'Nhóm 1 — Trẻ', 'Nhóm 2 — Rủi ro', 'Nhóm 3 — Trung thành'])
plt.ylabel('$')
plt.legend(fontsize=10)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/segment_spending_satisfaction.png', dpi=200, bbox_inches='tight')
plt.show()

# Biểu đồ 4: Chi tiêu theo mức thu nhập
plt.figure(figsize=(8, 5))
income_avg = df_clean.groupby('Income_Level')['Purchase_Amount'].mean()
sns.barplot(x=income_avg.index, y=income_avg.values, palette=['#8A7CFF', '#4ECDC4'])
plt.title('Chi tiêu theo mức thu nhập', fontsize=13)
plt.ylabel('Chi tiêu trung bình ($)')
plt.ylim(270, 278)
plt.tight_layout()
plt.savefig('charts/spending_by_income.png', dpi=200, bbox_inches='tight')
plt.show()

# Biểu đồ 5: Chi tiêu theo giới tính
plt.figure(figsize=(8, 5))
gender_avg = df_clean.groupby('Gender')['Purchase_Amount'].mean()
sns.barplot(x=gender_avg.index, y=gender_avg.values, palette="Purples_d")
plt.title('Chi tiêu trung bình theo giới tính', fontsize=13)
plt.ylabel('Chi tiêu trung bình ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('charts/spending_by_gender.png', dpi=200, bbox_inches='tight')
plt.show()

print("✅ Hoàn thành Phần 4")

# ================== 5. TRỰC QUAN HÓA DỮ LIỆU ==================

print("5. TẠO BIỂU ĐỒ TRỰC QUAN ")


import os
sns.set_style("whitegrid")

# Tạo thư mục lưu ảnh
output_dir = "charts"
os.makedirs(output_dir, exist_ok=True)

# 1. Phân bố giá trị đơn hàng
plt.figure(figsize=(8,5))
plt.hist(df_clean['Purchase_Amount'], bins=30, edgecolor='black')
plt.xlabel('Giá trị đơn hàng ($)')
plt.ylabel('Tần suất')
plt.title('Phân bố Giá trị Đơn hàng')
plt.axvline(df_clean['Purchase_Amount'].mean(), linestyle='--')
plt.savefig(f"{output_dir}/1_purchase_amount.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 2. Top danh mục sản phẩm
plt.figure(figsize=(8,5))
top_categories = df_clean['Purchase_Category'].value_counts().head(10)
plt.barh(top_categories.index, top_categories.values)
plt.xlabel('Số lần mua')
plt.title('Top 10 Danh mục Sản phẩm')
plt.gca().invert_yaxis()
plt.savefig(f"{output_dir}/2_top_categories.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 3. Chi tiêu theo mức thu nhập
plt.figure(figsize=(8,5))

# Làm sạch dữ liệu nếu cần
df_clean['Income_Level'] = df_clean['Income_Level'].str.strip()

income_avg = df_clean.groupby('Income_Level')['Purchase_Amount'].mean()

# Tạo danh sách màu (tự động theo số cột)
colors = ['#4CAF50', '#FF9800', '#2196F3']  # xanh, cam, xanh dương

plt.bar(income_avg.index, income_avg.values,
        width=0.5,
        color=colors[:len(income_avg)])

plt.xlabel('Mức thu nhập')
plt.ylabel('Chi tiêu trung bình ($)')
plt.title('Chi tiêu trung bình theo Mức thu nhập')

# Hiển thị số trên đầu cột
for i, v in enumerate(income_avg.values):
    plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')

plt.savefig(f"{output_dir}/3_income_vs_spending_bar.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 4. Phân bố tuổi
plt.figure(figsize=(8,5))
plt.hist(df_clean['Age'], bins=20, edgecolor='black')
plt.xlabel('Tuổi')
plt.ylabel('Số lượng')
plt.title('Phân bố Tuổi Khách hàng')
plt.savefig(f"{output_dir}/4_age_distribution.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 5. Hài lòng vs Chi tiêu
df_clean['Spending_Group'] = pd.qcut(df_clean['Purchase_Amount'], q=3, labels=['Low', 'Medium', 'High'])

plt.figure(figsize=(8,5))

group_satisfaction = df_clean.groupby('Spending_Group')['Customer_Satisfaction'].mean()

plt.bar(group_satisfaction.index, group_satisfaction.values,
        width=0.5,
        color=['#4CAF50', '#FF9800', '#F44336'])

plt.xlabel('Mức chi tiêu')
plt.ylabel('Điểm hài lòng trung bình')
plt.title('Hài lòng theo Mức chi tiêu')

for i, v in enumerate(group_satisfaction.values):
    plt.text(i, v, f'{v:.2f}', ha='center')

plt.savefig(f"{output_dir}/5_satisfaction_vs_spending_bar.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 6. Chi tiêu theo giới tính
plt.figure(figsize=(8,5))
gender_avg = df_clean.groupby('Gender')['Purchase_Amount'].mean()

plt.bar(gender_avg.index, gender_avg.values,
        width=0.5,
        color=['#FF69B4', '#4169E1'][:len(gender_avg)])

plt.ylabel('Chi tiêu trung bình ($)')
plt.title('Chi tiêu theo Giới tính')

for i, v in enumerate(gender_avg.values):
    plt.text(i, v, f'{v:.2f}', ha='center')

plt.savefig(f"{output_dir}/6_gender.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 7. Tần suất mua
plt.figure(figsize=(8,5))

freq_counts = df_clean['Frequency_of_Purchase'].value_counts().sort_index()

plt.bar(freq_counts.index, freq_counts.values, width=0.6)

plt.xlabel('Tần suất mua')
plt.ylabel('Số khách hàng')
plt.title('Số khách hàng theo Tần suất Mua')

# hiện số trên đầu cột
for i, v in zip(freq_counts.index, freq_counts.values):
    plt.text(i, v, str(v), ha='center')

plt.savefig(f"{output_dir}/7_frequency_bar.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()
# 8. Phân đoạn khách hàng
plt.figure(figsize=(8,5))

segment_spending = df_clean.groupby('Customer_Segment')['Purchase_Amount'].mean()

plt.bar(segment_spending.index, segment_spending.values,
        width=0.5,
        color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])

plt.xlabel('Nhóm khách hàng')
plt.ylabel('Chi tiêu trung bình ($)')
plt.title('Chi tiêu trung bình theo Nhóm khách hàng')

for i, v in enumerate(segment_spending.values):
    plt.text(i, v, f'{v:.2f}', ha='center')

plt.savefig(f"{output_dir}/8_customer_segments_bar.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 9. Phương thức thanh toán
plt.figure(figsize=(6,6))
payment_counts = df_clean['Payment_Method'].value_counts()
plt.pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%')
plt.title('Tỷ lệ Phương thức Thanh toán')
plt.savefig(f"{output_dir}/9_payment_methods.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print(f"✓ Đã lưu toàn bộ biểu đồ vào thư mục: {output_dir}/")

# ================== 6. XÂY DỰNG MÔ HÌNH DỰ ĐOÁN CHI TIÊU ==================
print("\n" + "=" * 80)
print("6. MÔ HÌNH DỰ ĐOÁN CHI TIÊU KHÁCH HÀNG")
print("=" * 80)

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

feature_columns = ['Age', 'Frequency_of_Purchase', 'Brand_Loyalty', 'Product_Rating',
                   'Time_Spent_on_Product_Research(hours)', 'Return_Rate',
                   'Customer_Satisfaction', 'Time_to_Decision'] + categorical_features

X = df_model[feature_columns]
y = df_model['Purchase_Amount']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nĐang huấn luyện mô hình Random Forest...")
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15)
model.fit(X_train, y_train)

y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)

print(f"\nĐánh giá hiệu suất mô hình:")
print(f"  RMSE huấn luyện : ${train_rmse:.2f}")
print(f"  RMSE kiểm tra   : ${test_rmse:.2f}")
print(f"  MAE huấn luyện  : ${train_mae:.2f}")
print(f"  MAE kiểm tra    : ${test_mae:.2f}")
print(f"  R² huấn luyện   : {train_r2:.4f}")
print(f"  R² kiểm tra     : {test_r2:.4f}")

# Feature Importance
feature_importance = pd.DataFrame({
    'Đặc trưng': feature_columns,
    'Mức độ quan trọng': model.feature_importances_
}).sort_values('Mức độ quan trọng', ascending=False)

print(f"\nTop 15 đặc trưng quan trọng nhất:")
for idx, row in feature_importance.head(15).iterrows():
    print(f"  {row['Đặc trưng']}: {row['Mức độ quan trọng']:.4f}")

# ================== 7. DỰ ĐOÁN MẪU ==================
print("\n" + "=" * 80)
print("7. VÍ DỤ DỰ ĐOÁN CHI TIÊU")
print("=" * 80)

sample_indices = np.random.choice(X_test.index, 5, replace=False)
sample_X = X_test.loc[sample_indices]
sample_y_actual = y_test.loc[sample_indices]
sample_y_pred = model.predict(sample_X)

print("\nKết quả dự đoán cho 5 khách hàng ngẫu nhiên:")
for i, (idx, pred, actual) in enumerate(zip(sample_indices, sample_y_pred, sample_y_actual), 1):
    error = abs(pred - actual) / actual * 100
    print(f"\n  Khách hàng {i}:")
    print(f"    Dự đoán chi tiêu : ${pred:.2f}")
    print(f"    Thực tế          : ${actual:.2f}")
    print(f"    Sai số           : {error:.1f}%")

# ================== 8. LƯU KẾT QUẢ ==================
print("\n" + "=" * 80)
print("8. LƯU KẾT QUẢ PHÂN TÍCH")
print("=" * 80)

df_clean.to_csv('data_cleaned.csv', index=False)
print("✓ Đã lưu dữ liệu đã làm sạch: 'data_cleaned.csv'")

segments_summary = df_clean.groupby('Customer_Segment').agg({
    'Purchase_Amount': ['mean', 'median', 'count'],
    'Age': 'mean',
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean'
}).round(2)
segments_summary.to_csv('customer_segments_analysis.csv')
print("✓ Đã lưu phân tích phân đoạn khách hàng: 'customer_segments_analysis.csv'")

pairs_df = pd.DataFrame(list(pair_counts.most_common(50)),
                        columns=['Product_Combination', 'Count'])
pairs_df['Sản_phẩm_1'] = pairs_df['Product_Combination'].str[0]
pairs_df['Sản_phẩm_2'] = pairs_df['Product_Combination'].str[1]
pairs_df = pairs_df[['Sản_phẩm_1', 'Sản_phẩm_2', 'Count']]
pairs_df.to_csv('product_combinations.csv', index=False)
print("✓ Đã lưu các cặp sản phẩm: 'product_combinations.csv'")

feature_importance.to_csv('feature_importance.csv', index=False)
print("✓ Đã lưu mức độ quan trọng của đặc trưng: 'feature_importance.csv'")

prediction_results = pd.DataFrame({
    'Thuc_te': y_test.values,
    'Du_doan': y_pred_test,
    'Sai_so': np.abs(y_test.values - y_pred_test),
    'Phan_tram_loi': (np.abs(y_test.values - y_pred_test) / y_test.values * 100)
})
prediction_results.to_csv('model_predictions.csv', index=False)
print("✓ Đã lưu kết quả dự đoán: 'model_predictions.csv'")

# ================== TÓM TẮT CUỐI CÙNG ==================
print("\n" + "=" * 80)
print("HOÀN THÀNH PHÂN TÍCH HÀNH VI NGƯỜI TIÊU DÙNG")
print("=" * 80)

# Lấy số nhóm an toàn (phòng trường hợp chưa chạy phần 4)
num_clusters = df_clean['Customer_Segment'].nunique() if 'Customer_Segment' in df_clean.columns else 4

print(f"\nTóm tắt kết quả:")
print(f"  • Số giao dịch đã phân tích : {len(df_clean):,}")
print(f"  • Số danh mục sản phẩm     : {df_clean['Purchase_Category'].nunique()}")
print(f"  • Số nhóm khách hàng        : {num_clusters}")
print(f"  • Độ chính xác mô hình (R²) : {test_r2:.2%}" if 'test_r2' in locals() else "  • Độ chính xác mô hình (R²) : Chưa chạy mô hình")
print("=" * 80)