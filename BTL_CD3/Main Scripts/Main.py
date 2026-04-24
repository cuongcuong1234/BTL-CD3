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

# ================== 1. TẢI & LÀM SẠCH DỮ LIỆU ==================
print("="*60)
print("1. TẢI VÀ LÀM SẠCH DỮ LIỆU")
print("="*60)

df = pd.read_csv('BTL_CD3/data Files/Ecommerce_Consumer_Behavior_Analysis_Data.csv')
print(f"Kích thước dữ liệu gốc: {df.shape}")
print(f"\nGiá trị thiếu:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# Tạo bản sao để xử lý
df_sach = df.copy()

# Làm sạch cột Purchase_Amount: Loại bỏ "$" và chuyển sang số thực
df_sach['Purchase_Amount'] = df_sach['Purchase_Amount'].str.replace('$', '').astype(float)

# Xử lý giá trị thiếu
# Với Social_Media_Influence và Engagement_with_Ads, điền bằng mode (giá trị xuất hiện nhiều nhất)
df_sach['Social_Media_Influence'].fillna(df_sach['Social_Media_Influence'].mode()[0], inplace=True)
df_sach['Engagement_with_Ads'].fillna(df_sach['Engagement_with_Ads'].mode()[0], inplace=True)

# Xóa bản ghi trùng lặp nếu có
so_hang_ban_dau = len(df_sach)
df_sach.drop_duplicates(inplace=True)
print(f"\nĐã xóa {so_hang_ban_dau - len(df_sach)} dòng trùng lặp")

# Kiểm tra lại kiểu dữ liệu
print(f"\nKích thước dữ liệu sau làm sạch: {df_sach.shape}")
print(f"Tổng số giá trị thiếu sau làm sạch: {df_sach.isnull().sum().sum()}")
print("✓ Làm sạch dữ liệu thành công!")

# ================== 2. PHÂN TÍCH THĂM DÒ DỮ LIỆU ==================
print("\n" + "="*60)
print("2. PHÂN TÍCH THĂM DÒ DỮ LIỆU")
print("="*60)

print(f"\nThống kê cơ bản:")
print(f"  - Giá trị mua hàng trung bình: ${df_sach['Purchase_Amount'].mean():.2f}")
print(f"  - Giá trị mua hàng trung vị: ${df_sach['Purchase_Amount'].median():.2f}")
print(f"  - Giá trị mua hàng nhỏ nhất: ${df_sach['Purchase_Amount'].min():.2f}")
print(f"  - Giá trị mua hàng lớn nhất: ${df_sach['Purchase_Amount'].max():.2f}")
print(f"\n  - Độ tuổi trung bình của khách hàng: {df_sach['Age'].mean():.1f} tuổi")
print(f"  - Mức độ hài lòng trung bình: {df_sach['Customer_Satisfaction'].mean():.2f}/10")

print(f"\nCác danh mục sản phẩm hàng đầu:")
print(df_sach['Purchase_Category'].value_counts().head(10))

print(f"\nPhân bố mức thu nhập:")
print(df_sach['Income_Level'].value_counts())

# ================== 3. CÁC SẢN PHẨM THƯỜNG ĐƯỢC MUA CÙNG NHAU ==================
print("\n" + "="*60)
print("3. PHÂN TÍCH GIỎ HÀNG - CÁC SẢN PHẨM ĐƯỢC MUA CÙNG NHAU")
print("="*60)

# Nhóm theo khách hàng để tìm ra các sản phẩm mỗi khách đã mua
san_pham_cua_khach = df_sach.groupby('Customer_ID')['Purchase_Category'].apply(list).values

# Tìm các cặp sản phẩm
cap_san_pham = []
dem_san_pham = Counter()

for san_phams in san_pham_cua_khach:
    cac_san_pham_duy_nhat = list(set(san_phams))
    dem_san_pham.update(cac_san_pham_duy_nhat)
    if len(cac_san_pham_duy_nhat) > 1:
        cap = list(combinations(sorted(cac_san_pham_duy_nhat), 2))
        cap_san_pham.extend(cap)

# Đếm tần suất các cặp
dem_cap = Counter(cap_san_pham)

print(f"\n15 tổ hợp sản phẩm hàng đầu được mua cùng nhau:")
for idx, (cap, so_lan) in enumerate(dem_cap.most_common(15), 1):
    sp1, sp2 = cap
    print(f"  {idx}. {sp1} + {sp2}: {so_lan} lần")

# Các sản phẩm riêng lẻ hàng đầu
print(f"\n10 danh mục được mua nhiều nhất:")
for idx, (san_pham, so_lan) in enumerate(dem_san_pham.most_common(10), 1):
    ty_le = (so_lan / sum(dem_san_pham.values())) * 100
    print(f"  {idx}. {san_pham}: {so_lan} lượt mua ({ty_le:.1f}%)")

# ================== 4. PHÂN KHÚC KHÁCH HÀNG & PHÂN TÍCH CHI TIÊU ==================
print("\n" + "="*60)
print("4. PHÂN KHÚC KHÁCH HÀNG & PHÂN TÍCH CHI TIÊU")
print("="*60)

# Chuẩn bị các đặc trưng cho phân khúc
cac_dac_trung_phan_khuc = ['Age', 'Purchase_Amount', 'Frequency_of_Purchase', 
                           'Customer_Satisfaction', 'Brand_Loyalty']

X_phan_khuc = df_sach[cac_dac_trung_phan_khuc].copy()
bo_chuan_hoa = StandardScaler()
X_phan_khuc_chuan_hoa = bo_chuan_hoa.fit_transform(X_phan_khuc)

# Phân cụm K-means (4 phân khúc)
so_cum = 4
kmeans = KMeans(n_clusters=so_cum, random_state=42, n_init=10)
df_sach['Customer_Segment'] = kmeans.fit_predict(X_phan_khuc_chuan_hoa)

# Phân tích các phân khúc
print(f"\nCác phân khúc khách hàng (n={so_cum}):")
for phan_khuc in range(so_cum):
    du_lieu_phan_khuc = df_sach[df_sach['Customer_Segment'] == phan_khuc]
    print(f"\n  Phân khúc {phan_khuc} ({len(du_lieu_phan_khuc)} khách hàng):")
    print(f"    - Độ tuổi TB: {du_lieu_phan_khuc['Age'].mean():.1f}")
    print(f"    - Chi tiêu TB: ${du_lieu_phan_khuc['Purchase_Amount'].mean():.2f}")
    print(f"    - Tần suất mua TB: {du_lieu_phan_khuc['Frequency_of_Purchase'].mean():.1f}")
    print(f"    - Mức hài lòng TB: {du_lieu_phan_khuc['Customer_Satisfaction'].mean():.2f}/10")
    print(f"    - Lòng trung thành TB: {du_lieu_phan_khuc['Brand_Loyalty'].mean():.2f}")

# Phân tích chi tiêu theo mức thu nhập
print(f"\nPhân tích chi tiêu theo mức thu nhập:")
chi_tieu_theo_thu_nhap = df_sach.groupby('Income_Level').agg({
    'Purchase_Amount': ['mean', 'median', 'sum', 'count']
}).round(2)
chi_tieu_theo_thu_nhap.columns = ['Trung_bình', 'Trung_vị', 'Tổng', 'Số_lượng']
print(chi_tieu_theo_thu_nhap.sort_values('Trung_bình', ascending=False))

# Phân tích chi tiêu theo giới tính
print(f"\nPhân tích chi tiêu theo giới tính:")
chi_tieu_theo_gioi_tinh = df_sach.groupby('Gender').agg({
    'Purchase_Amount': ['mean', 'median', 'sum', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)
chi_tieu_theo_gioi_tinh.columns = ['Trung_bình', 'Trung_vị', 'Tổng', 'Số_lượng', 'Hài_lòng']
print(chi_tieu_theo_gioi_tinh)

# ================== 5. TRỰC QUAN HÓA DỮ LIỆU ==================
print("\n" + "="*60)
print("5. TẠO CÁC BIỂU ĐỒ TRỰC QUAN")
print("="*60)

# Thiết lập style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 12)

fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle('Phân Tích Hành Vi Người Tiêu Dùng Thương Mại Điện Tử', fontsize=20, fontweight='bold', y=0.995)

# 1. Phân bố giá trị đơn hàng
axes[0, 0].hist(df_sach['Purchase_Amount'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Giá trị đơn hàng ($)')
axes[0, 0].set_ylabel('Tần suất')
axes[0, 0].set_title('Phân bố giá trị đơn hàng')
axes[0, 0].axvline(df_sach['Purchase_Amount'].mean(), color='red', linestyle='--', label=f'TB: ${df_sach["Purchase_Amount"].mean():.2f}')
axes[0, 0].legend()

# 2. 10 danh mục sản phẩm hàng đầu
top_danh_muc = df_sach['Purchase_Category'].value_counts().head(10)
axes[0, 1].barh(range(len(top_danh_muc)), top_danh_muc.values, color='coral')
axes[0, 1].set_yticks(range(len(top_danh_muc)))
axes[0, 1].set_yticklabels(top_danh_muc.index)
axes[0, 1].set_xlabel('Số lượt mua')
axes[0, 1].set_title('10 danh mục sản phẩm hàng đầu')
axes[0, 1].invert_yaxis()

# 3. Chi tiêu theo mức thu nhập
thu_tu_thu_nhap = ['Low', 'Medium', 'High']
du_lieu_thu_nhap = df_sach[df_sach['Income_Level'].isin(thu_tu_thu_nhap)].copy()
sns.boxplot(x='Income_Level', y='Purchase_Amount', data=du_lieu_thu_nhap, order=thu_tu_thu_nhap, ax=axes[0, 2], palette='Set2')
axes[0, 2].set_ylabel('Giá trị đơn hàng ($)')
axes[0, 2].set_xlabel('Mức thu nhập')
axes[0, 2].set_title('Chi tiêu theo mức thu nhập')

# 4. Phân bố độ tuổi khách hàng
axes[1, 0].hist(df_sach['Age'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('Tuổi')
axes[1, 0].set_ylabel('Tần suất')
axes[1, 0].set_title('Phân bố độ tuổi khách hàng')

# 5. Mức độ hài lòng so với giá trị đơn hàng
bubble = axes[1, 1].scatter(df_sach['Purchase_Amount'], df_sach['Customer_Satisfaction'], 
                            c=df_sach['Age'], cmap='viridis', alpha=0.6, s=50)
axes[1, 1].set_xlabel('Giá trị đơn hàng ($)')
axes[1, 1].set_ylabel('Mức độ hài lòng')
axes[1, 1].set_title('Hài lòng vs Chi tiêu (tô màu theo độ tuổi)')
thanh_mau = plt.colorbar(bubble, ax=axes[1, 1])
thanh_mau.set_label('Tuổi')

# 6. Chi tiêu theo giới tính
chi_tieu_tb_theo_gioi = df_sach.groupby('Gender')['Purchase_Amount'].mean()
mau_sac = ['#FF69B4', '#4169E1']
axes[1, 2].bar(chi_tieu_tb_theo_gioi.index, chi_tieu_tb_theo_gioi.values, color=mau_sac, alpha=0.7, edgecolor='black')
axes[1, 2].set_ylabel('Giá trị đơn hàng trung bình ($)')
axes[1, 2].set_title('Chi tiêu trung bình theo giới tính')
for i, v in enumerate(chi_tieu_tb_theo_gioi.values):
    axes[1, 2].text(i, v + 5, f'${v:.2f}', ha='center', fontweight='bold')

# 7. Phân bố tần suất mua hàng
axes[2, 0].hist(df_sach['Frequency_of_Purchase'], bins=15, color='purple', edgecolor='black', alpha=0.7)
axes[2, 0].set_xlabel('Tần suất mua hàng')
axes[2, 0].set_ylabel('Số lượng khách hàng')
axes[2, 0].set_title('Phân bố tần suất mua hàng')

# 8. Tổng quan các phân khúc khách hàng (biểu diễn 3D trên 2D)
chi_tieu_tb_phan_khuc = df_sach.groupby('Customer_Segment')['Purchase_Amount'].mean()
so_luong_phan_khuc = df_sach['Customer_Segment'].value_counts().sort_index()
mau_phan_khuc = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
axes[2, 1].scatter(so_luong_phan_khuc.values, chi_tieu_tb_phan_khuc.values, 
                   s=[x*10 for x in so_luong_phan_khuc.values], 
                   c=mau_phan_khuc, alpha=0.6, edgecolors='black', linewidth=2)
for i, pk in enumerate(range(so_cum)):
    axes[2, 1].annotate(f'Phân khúc {pk}', 
                       (so_luong_phan_khuc[pk], chi_tieu_tb_phan_khuc[pk]),
                       xytext=(5, 5), textcoords='offset points', fontweight='bold')
axes[2, 1].set_xlabel('Số lượng khách hàng')
axes[2, 1].set_ylabel('Chi tiêu trung bình ($)')
axes[2, 1].set_title('Tổng quan các phân khúc khách hàng')

# 9. Phương thức thanh toán
so_luong_thanh_toan = df_sach['Payment_Method'].value_counts()
axes[2, 2].pie(so_luong_thanh_toan.values, labels=so_luong_thanh_toan.index, autopct='%1.1f%%', startangle=90)
axes[2, 2].set_title('Phân bố phương thức thanh toán')

plt.tight_layout()
plt.savefig('phan_tich_hanh_vi_nguoi_tieu_dung.png', dpi=300, bbox_inches='tight')
print("✓ Đã lưu biểu đồ trực quan với tên 'phan_tich_hanh_vi_nguoi_tieu_dung.png'")
plt.close()

# ================== 6. MÔ HÌNH DỰ ĐOÁN - DỰ ĐOÁN CHI TIÊU ==================
print("\n" + "="*60)
print("6. MÔ HÌNH DỰ ĐOÁN - DỰ ĐOÁN CHI TIÊU CỦA KHÁCH HÀNG")
print("="*60)

# Chuẩn bị các đặc trưng cho dự đoán
# Mã hóa các biến phân loại
tu_dien_ma_hoa = {}
cac_dac_trung_phân_loai = ['Gender', 'Income_Level', 'Marital_Status', 'Education_Level', 
                          'Occupation', 'Location', 'Purchase_Channel', 'Social_Media_Influence',
                          'Discount_Sensitivity', 'Device_Used_for_Shopping', 'Payment_Method',
                          'Time_of_Purchase', 'Purchase_Intent', 'Shipping_Preference']

df_mo_hinh = df_sach.copy()

for dac_trung in cac_dac_trung_phân_loai:
    ma_hoa = LabelEncoder()
    df_mo_hinh[dac_trung] = ma_hoa.fit_transform(df_mo_hinh[dac_trung])
    tu_dien_ma_hoa[dac_trung] = ma_hoa

# Chọn các đặc trưng cho mô hình
cac_cot_dac_trung = ['Age', 'Frequency_of_Purchase', 'Brand_Loyalty', 'Product_Rating',
                     'Time_Spent_on_Product_Research(hours)', 'Return_Rate',
                     'Customer_Satisfaction', 'Time_to_Decision'] + cac_dac_trung_phân_loai

X = df_mo_hinh[cac_cot_dac_trung]
y = df_mo_hinh['Purchase_Amount']

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình
print("\nĐang huấn luyện mô hình Random Forest...")
mo_hinh = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15)
mo_hinh.fit(X_train, y_train)

# Dự đoán
y_pred_train = mo_hinh.predict(X_train)
y_pred_test = mo_hinh.predict(X_test)

# Các chỉ số đánh giá
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)

print(f"\nHiệu suất mô hình:")
print(f"  RMSE trên tập huấn luyện: ${train_rmse:.2f}")
print(f"  RMSE trên tập kiểm tra: ${test_rmse:.2f}")
print(f"  MAE trên tập huấn luyện: ${train_mae:.2f}")
print(f"  MAE trên tập kiểm tra: ${test_mae:.2f}")
print(f"  R² trên tập huấn luyện: {train_r2:.4f}")
print(f"  R² trên tập kiểm tra: {test_r2:.4f}")

# Mức độ quan trọng của các đặc trưng
muc_do_quan_trong = pd.DataFrame({
    'Đặc_trưng': cac_cot_dac_trung,
    'Độ_quan_trọng': mo_hinh.feature_importances_
}).sort_values('Độ_quan_trọng', ascending=False)

print(f"\n15 đặc trưng quan trọng nhất:")
for idx, dong in muc_do_quan_trong.head(15).iterrows():
    print(f"  {dong['Đặc_trưng']}: {dong['Độ_quan_trọng']:.4f}")

# ================== 7. VÍ DỤ DỰ ĐOÁN ==================
print("\n" + "="*60)
print("7. VÍ DỤ DỰ ĐOÁN - CHI TIÊU CỦA KHÁCH HÀNG MẪU")
print("="*60)

# Tạo các dự đoán mẫu
cac_chi_mau = np.random.choice(X_test.index, 5, replace=False)
X_mau = X_test.loc[cac_chi_mau]
y_thuc_mau = y_test.loc[cac_chi_mau]
y_du_doan_mau = mo_hinh.predict(X_mau)

print("\nCác dự đoán mẫu (so với chi tiêu thực tế):")
for i, (idx, du_doan, thuc_te) in enumerate(zip(cac_chi_mau, y_du_doan_mau, y_thuc_mau), 1):
    sai_so = abs(du_doan - thuc_te) / thuc_te * 100
    print(f"  Khách hàng {i}:")
    print(f"    Chi tiêu dự đoán: ${du_doan:.2f}")
    print(f"    Chi tiêu thực tế: ${thuc_te:.2f}")
    print(f"    Sai số: {sai_so:.1f}%\n")

# ================== 8. LƯU KẾT QUẢ ==================
print("="*60)
print("8. LƯU KẾT QUẢ")
print("="*60)

# Lưu dữ liệu đã làm sạch
df_sach.to_csv('du_lieu_da_sach.csv', index=False)
print("✓ Đã lưu dữ liệu đã làm sạch với tên 'du_lieu_da_sach.csv'")

# Lưu phân tích phân khúc khách hàng
tom_tat_phan_khuc = df_sach.groupby('Customer_Segment').agg({
    'Purchase_Amount': ['mean', 'median', 'count'],
    'Age': 'mean',
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean'
}).round(2)
tom_tat_phan_khuc.to_csv('phan_tich_phan_khuc_khach_hang.csv')
print("✓ Đã lưu phân tích phân khúc khách hàng với tên 'phan_tich_phan_khuc_khach_hang.csv'")

# Lưu các tổ hợp sản phẩm hàng đầu
df_cap = pd.DataFrame(list(dem_cap.most_common(50)), 
                      columns=['Tổ_hợp_sản_phẩm', 'Số_lần'])
df_cap['Sản_phẩm_1'] = df_cap['Tổ_hợp_sản_phẩm'].str[0]
df_cap['Sản_phẩm_2'] = df_cap['Tổ_hợp_sản_phẩm'].str[1]
df_cap = df_cap[['Sản_phẩm_1', 'Sản_phẩm_2', 'Số_lần']]
df_cap.to_csv('cac_cap_san_pham.csv', index=False)
print("✓ Đã lưu các cặp sản phẩm với tên 'cac_cap_san_pham.csv'")

# Lưu mức độ quan trọng của các đặc trưng
muc_do_quan_trong.to_csv('muc_do_quan_trong_dac_trung.csv', index=False)
print("✓ Đã lưu mức độ quan trọng của đặc trưng với tên 'muc_do_quan_trong_dac_trung.csv'")

# Lưu kết quả dự đoán
ket_qua_du_doan = pd.DataFrame({
    'Chi_tieu_thuc_te': y_test.values,
    'Chi_tieu_du_doan': y_pred_test,
    'Sai_so_tuyet_doi': np.abs(y_test.values - y_pred_test),
    'Sai_so_phan_tram': (np.abs(y_test.values - y_pred_test) / y_test.values * 100)
})
ket_qua_du_doan.to_csv('du_doan_cua_mo_hinh.csv', index=False)
print("✓ Đã lưu dự đoán của mô hình với tên 'du_doan_cua_mo_hinh.csv'")

# ================== TỔNG KẾT ==================
print("\n" + "="*60)
print("PHÂN TÍCH HOÀN TẤT!")
print("="*60)
print(f"\n✓ Các đầu ra đã tạo:")
print(f"  1. phan_tich_hanh_vi_nguoi_tieu_dung.png - Biểu đồ trực quan 9 bảng")
print(f"  2. du_lieu_da_sach.csv - Dữ liệu giao dịch đã làm sạch")
print(f"  3. phan_tich_phan_khuc_khach_hang.csv - Thông tin phân khúc khách hàng")
print(f"  4. cac_cap_san_pham.csv - Các cặp sản phẩm hàng đầu")
print(f"  5. muc_do_quan_trong_dac_trung.csv - Mức độ quan trọng của các đặc trưng")
print(f"  6. du_doan_cua_mo_hinh.csv - Dự đoán chi tiêu khách hàng")
print(f"\n✓ Tóm tắt phân tích:")
print(f"  - Đã phân tích {len(df_sach)} giao dịch")
print(f"  - {df_sach['Purchase_Category'].nunique()} danh mục sản phẩm")
print(f"  - Đã xác định {so_cum} phân khúc khách hàng")
print(f"  - Mô hình đạt độ chính xác {test_r2:.2%} trên tập kiểm tra")
print("="*60)