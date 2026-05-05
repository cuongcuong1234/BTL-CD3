import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# ================== PHÂN TÍCH NÂNG CAO & TRỰC QUAN HÓA ==================
print("="*60)
print("PHÂN TÍCH NÂNG CAO HÀNH VI KHÁCH HÀNG")
print("="*60)

# Đọc dữ liệu đã làm sạch
du_lieu = pd.read_csv('data_cleaned.csv')

# ================== 1. PHÂN TÍCH GIÁ TRỊ VÒNG ĐỜI KHÁCH HÀNG ==================
print("\n1. PHÂN TÍCH GIÁ TRỊ VÒNG ĐỜI KHÁCH HÀNG")
print("-"*60)

# Tính CLV
du_lieu['Gia_tri_vong_doi'] = (
    du_lieu['Purchase_Amount'] *
    du_lieu['Frequency_of_Purchase'] *
    du_lieu['Customer_Satisfaction'] / 10
)

phan_tich_clv = du_lieu.groupby('Customer_Segment').agg({
    'Purchase_Amount': ['mean', 'sum'],
    'Frequency_of_Purchase': 'mean',
    'Customer_Satisfaction': 'mean',
    'Gia_tri_vong_doi': ['mean', 'sum']
}).round(2)

print("\nGiá trị vòng đời theo phân khúc:")
print(phan_tich_clv)

# Top khách hàng
top_khach_hang = du_lieu.nlargest(
    20, 'Gia_tri_vong_doi'
)[[
    'Customer_ID',
    'Age',
    'Income_Level',
    'Purchase_Amount',
    'Frequency_of_Purchase',
    'Customer_Satisfaction',
    'Gia_tri_vong_doi'
]]

print("\n20 khách hàng có giá trị vòng đời cao nhất:")
for _, dong in top_khach_hang.iterrows():
    print(
        f"{dong['Customer_ID']} | "
        f"CLV=${dong['Gia_tri_vong_doi']:.2f} | "
        f"Tuổi: {dong['Age']} | "
        f"Thu nhập: {dong['Income_Level']}"
    )


# ================== 2. PHÂN TÍCH RỦI RO RỜI BỎ ==================
print("\n2. PHÂN TÍCH RỦI RO RỜI BỎ")
print("-"*60)

nguong_rui_ro = du_lieu['Customer_Satisfaction'].quantile(0.33)

du_lieu['Rui_ro_roi_bo'] = (
    du_lieu['Customer_Satisfaction'] <= nguong_rui_ro
)

thong_ke_rui_ro = du_lieu['Rui_ro_roi_bo'].value_counts()

print(f"Rủi ro cao: {thong_ke_rui_ro[True]} khách hàng")
print(f"Rủi ro thấp: {thong_ke_rui_ro[False]} khách hàng")

du_lieu_rui_ro = du_lieu[
    du_lieu['Rui_ro_roi_bo'] == True
]


# ================== 3. PHÂN TÍCH KÊNH MUA HÀNG ==================
print("\n3. HIỆU SUẤT KÊNH MUA HÀNG")
print("-"*60)

phan_tich_kenh = du_lieu.groupby('Purchase_Channel').agg({
    'Purchase_Amount': ['mean', 'sum', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean',
    'Brand_Loyalty': 'mean'
}).round(2)

print(phan_tich_kenh)


# ================== 4. THỜI ĐIỂM MUA HÀNG ==================
print("\n4. PHÂN TÍCH THỜI ĐIỂM MUA HÀNG")
print("-"*60)

phan_tich_thoi_gian = du_lieu.groupby('Time_of_Purchase').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)

print(phan_tich_thoi_gian)


# ================== 5. THIẾT BỊ MUA HÀNG ==================
print("\n5. PHÂN TÍCH THIẾT BỊ MUA HÀNG")
print("-"*60)

phan_tich_thiet_bi = du_lieu.groupby(
    'Device_Used_for_Shopping'
).agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean'
}).round(2)

print(phan_tich_thiet_bi)


# ================== 6. CHƯƠNG TRÌNH THÂN THIẾT ==================
print("\n6. HIỆU QUẢ CHƯƠNG TRÌNH THÀNH VIÊN")
print("-"*60)

phan_tich_thanh_vien = du_lieu.groupby(
    'Customer_Loyalty_Program_Member'
).agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean',
    'Brand_Loyalty': 'mean'
}).round(2)

print(phan_tich_thanh_vien)


# ================== 7. CHIẾN LƯỢC GIẢM GIÁ ==================
print("\n7. HIỆU QUẢ GIẢM GIÁ")
print("-"*60)

phan_tich_giam_gia = du_lieu.groupby(
    'Discount_Used'
).agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean'
}).round(2)

print(phan_tich_giam_gia)


# ================== 8. TRUNG THÀNH THƯƠNG HIỆU ==================
print("\n8. PHÂN TÍCH TRUNG THÀNH THƯƠNG HIỆU")
print("-"*60)

du_lieu['Muc_do_trung_thanh'] = pd.cut(
    du_lieu['Brand_Loyalty'],
    bins=[0, 2, 4, 6, 10],
    labels=[
        'Rất thấp',
        'Thấp',
        'Trung bình',
        'Cao'
    ]
)

phan_tich_trung_thanh = du_lieu.groupby(
    'Muc_do_trung_thanh'
).agg({
    'Purchase_Amount': 'mean',
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean'
}).round(2)

print(phan_tich_trung_thanh)


# ================== 9. THANH TOÁN ==================
print("\n9. PHƯƠNG THỨC THANH TOÁN")
print("-"*60)

phan_tich_thanh_toan = du_lieu.groupby(
    'Payment_Method'
).agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)

print(phan_tich_thanh_toan)


# ================== 10. TRỰC QUAN HÓA ==================
print("\nĐang tạo biểu đồ...")

fig, axes = plt.subplots(3, 3, figsize=(18, 15))

fig.suptitle(
    'PHÂN TÍCH HÀNH VI KHÁCH HÀNG',
    fontsize=18,
    fontweight='bold'
)

# Biểu đồ CLV
axes[0,0].hist(
    du_lieu['Gia_tri_vong_doi'],
    bins=30
)
axes[0,0].set_title("Phân bố giá trị vòng đời")

# Rủi ro rời bỏ
so_luong_rui_ro = du_lieu[
    'Rui_ro_roi_bo'
].value_counts()

axes[0,1].bar(
    ['Thấp', 'Cao'],
    [
        so_luong_rui_ro[False],
        so_luong_rui_ro[True]
    ]
)
axes[0,1].set_title("Rủi ro rời bỏ")

# Doanh thu theo kênh
doanh_thu_kenh = du_lieu.groupby(
    'Purchase_Channel'
)['Purchase_Amount'].sum()

axes[0,2].bar(
    doanh_thu_kenh.index,
    doanh_thu_kenh.values
)
axes[0,2].set_title("Doanh thu theo kênh")


plt.tight_layout()

plt.savefig(
    'bieu_do_phan_tich_nang_cao.png',
    dpi=300,
    bbox_inches='tight'
)

print("Đã lưu biểu đồ")


# ================== 11. LƯU FILE BÁO CÁO ==================

# Khách hàng rủi ro
du_lieu_rui_ro.to_csv(
    'bao_cao_khach_hang_rui_ro_roi_bo.csv',
    index=False
)

# Giá trị vòng đời
du_lieu.sort_values(
    'Gia_tri_vong_doi',
    ascending=False
).to_csv(
    'bao_cao_gia_tri_vong_doi_khach_hang.csv',
    index=False
)

# Kênh bán hàng
phan_tich_kenh.to_csv(
    'bao_cao_hieu_suat_kenh_ban_hang.csv'
)

# Thiết bị
phan_tich_thiet_bi.to_csv(
    'bao_cao_phan_tich_thiet_bi_mua_hang.csv'
)

print("\n" + "="*60)
print("HOÀN THÀNH PHÂN TÍCH")
print("="*60)