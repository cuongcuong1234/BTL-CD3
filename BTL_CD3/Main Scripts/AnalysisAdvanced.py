import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# ================== PHÂN TÍCH NÂNG CAO & TRỰC QUAN HÓA CHI TIẾT ==================
print("="*60)
print("PHÂN TÍCH NÂNG CAO - HIỂU BIẾT CHI TIẾT")
print("="*60)

# Tải dữ liệu đã làm sạch
df = pd.read_csv(r'D:\BTLCD3\BTL_CD3\data Files\data_cleaned.csv')

# ================== 1. PHÂN TÍCH GIÁ TRỊ VÒNG ĐỜI KHÁCH HÀNG ==================
print("\n1. PHÂN TÍCH GIÁ TRỊ VÒNG ĐỜI KHÁCH HÀNG (CLV)")
print("-" * 60)

# Tính toán các chỉ số CLV
df['CLV_Tiem_nang'] = df['Purchase_Amount'] * df['Frequency_of_Purchase'] * df['Customer_Satisfaction'] / 10

phan_tich_clv = df.groupby('Customer_Segment').agg({
    'Purchase_Amount': ['mean', 'sum'],
    'Frequency_of_Purchase': 'mean',
    'Customer_Satisfaction': 'mean',
    'CLV_Tiem_nang': ['mean', 'sum']
}).round(2)

print("\nCLV theo Phân khúc Khách hàng:")
print(phan_tich_clv)

# 20 khách hàng hàng đầu theo CLV
khach_hang_hang_dau = df.nlargest(20, 'CLV_Tiem_nang')[['Customer_ID', 'Age', 'Income_Level', 
                                                          'Purchase_Amount', 'Frequency_of_Purchase',
                                                          'Customer_Satisfaction', 'CLV_Tiem_nang']]
print("\n20 Khách hàng Hàng đầu theo Giá trị Vòng đời:")
for idx, dong in khach_hang_hang_dau.iterrows():
    print(f"  {dong['Customer_ID']}: CLV=${dong['CLV_Tiem_nang']:.2f} | "
          f"Tuổi: {dong['Age']} | Thu nhập: {dong['Income_Level']} | "
          f"Hài lòng: {dong['Customer_Satisfaction']}/10")

# ================== 2. PHÂN TÍCH RỦI RO RỜI BỎ ==================
print("\n\n2. PHÂN TÍCH RỦI RO RỜI BỎ")
print("-" * 60)

# Hài lòng thấp = rủi ro rời bỏ cao
nguong_rui_ro = df['Customer_Satisfaction'].quantile(0.33)
df['Rui_ro_roi_bo'] = df['Customer_Satisfaction'] <= nguong_rui_ro

thong_ke_rui_ro = df['Rui_ro_roi_bo'].value_counts()
print(f"\nKhách hàng theo Rủi ro Rời bỏ:")
print(f"  Rủi ro Cao (Hài lòng <= {nguong_rui_ro:.1f}): {thong_ke_rui_ro[True]} khách hàng")
print(f"  Rủi ro Thấp (Hài lòng > {nguong_rui_ro:.1f}): {thong_ke_rui_ro[False]} khách hàng")

# Phân khúc rủi ro cao
rui_ro_cao = df[df['Rui_ro_roi_bo']]
print(f"\nChân dung Khách hàng Rủi ro Cao:")
print(f"  - Độ tuổi Trung bình: {rui_ro_cao['Age'].mean():.1f}")
print(f"  - Chi tiêu Trung bình: ${rui_ro_cao['Purchase_Amount'].mean():.2f}")
print(f"  - Mức hài lòng Trung bình: {rui_ro_cao['Customer_Satisfaction'].mean():.2f}/10")
print(f"  - Mức Thu nhập Cao nhất: {rui_ro_cao['Income_Level'].mode()[0]}")
print(f"  - Địa điểm Cao nhất: {rui_ro_cao['Location'].mode()[0]}")

# ================== 3. HIỆU SUẤT KÊNH MUA HÀNG ==================
print("\n\n3. HIỆU SUẤT KÊNH MUA HÀNG")
print("-" * 60)

phan_tich_kenh = df.groupby('Purchase_Channel').agg({
    'Purchase_Amount': ['mean', 'sum', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean',
    'Brand_Loyalty': 'mean'
}).round(2)

phan_tich_kenh.columns = ['TB_Chi_tieu', 'Tong_Doanh_thu', 'So_luong_Giao_dich', 
                           'Hai_long', 'Ty_le_Tra_hang', 'Trung_thanh']
print("\nChỉ số Hiệu suất Kênh:")
print(phan_tich_kenh.sort_values('Tong_Doanh_thu', ascending=False))

# ================== 4. PHÂN TÍCH THỜI ĐIỂM MUA HÀNG ==================
print("\n\n4. PHÂN TÍCH THỜI ĐIỂM MUA HÀNG")
print("-" * 60)

phan_tich_thoi_gian = df.groupby('Time_of_Purchase').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)

phan_tich_thoi_gian.columns = ['TB_Chi_tieu', 'So_luong_Giao_dich', 'Hai_long']
print("\nPhân bố Thời điểm Mua hàng:")
print(phan_tich_thoi_gian.sort_values('So_luong_Giao_dich', ascending=False))

# ================== 5. PHÂN TÍCH THIẾT BỊ & NỀN TẢNG ==================
print("\n\n5. PHÂN TÍCH THIẾT BỊ & NỀN TẢNG")
print("-" * 60)

phan_tich_thiet_bi = df.groupby('Device_Used_for_Shopping').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean'
}).round(2)

phan_tich_thiet_bi.columns = ['TB_Chi_tieu', 'So_luong_Giao_dich', 'Hai_long', 'Tan_suat']
print("\nHiệu suất Thiết bị:")
print(phan_tich_thiet_bi.sort_values('So_luong_Giao_dich', ascending=False))

# ================== 6. TÁC ĐỘNG CỦA CHƯƠNG TRÌNH THÂN THIẾT ==================
print("\n\n6. HIỆU QUẢ CỦA CHƯƠNG TRÌNH KHÁCH HÀNG THÂN THIẾT")
print("-" * 60)

so_sanh_thuong_hieu = df.groupby('Customer_Loyalty_Program_Member').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean',
    'Brand_Loyalty': 'mean',
    'Return_Rate': 'mean'
}).round(2)

so_sanh_thuong_hieu.columns = ['TB_Chi_tieu', 'So_luong', 'Hai_long', 'Tan_suat', 
                                'Trung_thanh_thuong_hieu', 'Ty_le_Tra_hang']
so_sanh_thuong_hieu.index = ['Không_phải_Thành_viên', 'Thành_viên']

print("\nTác động của Chương trình Khách hàng Thân thiết:")
print(so_sanh_thuong_hieu)

gia_tang_tu_chuong_trinh = ((so_sanh_thuong_hieu.loc['Thành_viên', 'TB_Chi_tieu'] - 
                              so_sanh_thuong_hieu.loc['Không_phải_Thành_viên', 'TB_Chi_tieu']) / 
                             so_sanh_thuong_hieu.loc['Không_phải_Thành_viên', 'TB_Chi_tieu'] * 100)
print(f"\nMức tăng Chi tiêu từ Chương trình Thân thiết: {gia_tang_tu_chuong_trinh:+.1f}%")

# ================== 7. PHÂN TÍCH CHIẾN LƯỢC GIẢM GIÁ ==================
print("\n\n7. HIỆU QUẢ CỦA CHIẾN LƯỢC GIẢM GIÁ")
print("-" * 60)

phan_tich_giam_gia = df.groupby('Discount_Used').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean'
}).round(2)

phan_tich_giam_gia.columns = ['TB_Chi_tieu', 'So_luong', 'Hai_long', 'Ty_le_Tra_hang']
phan_tich_giam_gia.index = ['Không_Giảm_giá', 'Có_Giảm_giá']

print("\nPhân tích Tác động của Giảm giá:")
print(phan_tich_giam_gia)

# ================== 8. MÔ HÌNH TRUNG THÀNH THƯƠNG HIỆU ==================
print("\n\n8. PHÂN TÍCH TRUNG THÀNH THƯƠNG HIỆU")
print("-" * 60)

phan_khuc_trung_thanh = pd.cut(df['Brand_Loyalty'], bins=[0, 2, 4, 6, 10], 
                               labels=['Rất Thấp', 'Thấp', 'Trung_bình', 'Cao'])
df['Phan_khuc_Trung_thanh'] = phan_khuc_trung_thanh

chuyen_dung_trung_thanh = df.groupby('Phan_khuc_Trung_thanh').agg({
    'Purchase_Amount': 'mean',
    'Customer_Satisfaction': 'mean',
    'Frequency_of_Purchase': 'mean',
    'Return_Rate': 'mean'
}).round(2)

print("\nChân dung Trung thành Thương hiệu:")
print(chuyen_dung_trung_thanh)

print(f"\nPhân bố Mức độ Trung thành Thương hiệu:")
print(phan_khuc_trung_thanh.value_counts())

# ================== 9. SỞ THÍCH PHƯƠNG THỨC THANH TOÁN ==================
print("\n\n9. SỞ THÍCH PHƯƠNG THỨC THANH TOÁN")
print("-" * 60)

phan_tich_thanh_toan = df.groupby('Payment_Method').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).round(2)

phan_tich_thanh_toan.columns = ['TB_Chi_tieu', 'So_luong', 'Hai_long']
print("\nThống kê Phương thức Thanh toán:")
print(phan_tich_thanh_toan.sort_values('So_luong', ascending=False))

# ================== 10. TRỰC QUAN HÓA NÂNG CAO TOÀN DIỆN ==================
print("\n\n" + "="*60)
print("ĐANG TẠO TRỰC QUAN HÓA NÂNG CAO")
print("="*60)

fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle('Phân Tích Nâng Cao Hành Vi Người Tiêu Dùng Thương Mại Điện Tử', 
             fontsize=20, fontweight='bold', y=0.995)

# 1. Phân bố Giá trị Vòng đời Khách hàng
axes[0, 0].hist(df['CLV_Tiem_nang'], bins=30, color='darkgreen', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Giá trị Vòng đời ($)')
axes[0, 0].set_ylabel('Số lượng Khách hàng')
axes[0, 0].set_title('Phân bố Giá trị Vòng đời Khách hàng')
axes[0, 0].axvline(df['CLV_Tiem_nang'].mean(), color='red', linestyle='--', 
                   label=f'TB: ${df["CLV_Tiem_nang"].mean():.2f}')
axes[0, 0].legend()

# 2. Phân khúc Rủi ro Rời bỏ
mau_rui_ro = ['#2ecc71', '#e74c3c']
so_luong_rui_ro = df['Rui_ro_roi_bo'].value_counts()
axes[0, 1].bar(['Rủi ro Thấp', 'Rủi ro Cao'], [so_luong_rui_ro[False], so_luong_rui_ro[True]], 
              color=mau_rui_ro, edgecolor='black', alpha=0.7)
axes[0, 1].set_ylabel('Số lượng Khách hàng')
axes[0, 1].set_title('Phân khúc Rủi ro Rời bỏ')
for i, v in enumerate([so_luong_rui_ro[False], so_luong_rui_ro[True]]):
    axes[0, 1].text(i, v + 10, str(v), ha='center', fontweight='bold')

# 3. Hiệu suất Kênh
doanh_thu_theo_kenh = df.groupby('Purchase_Channel')['Purchase_Amount'].sum().sort_values(ascending=False)
axes[0, 2].barh(range(len(doanh_thu_theo_kenh)), doanh_thu_theo_kenh.values, color='steelblue', edgecolor='black')
axes[0, 2].set_yticks(range(len(doanh_thu_theo_kenh)))
axes[0, 2].set_yticklabels(doanh_thu_theo_kenh.index)
axes[0, 2].set_xlabel('Tổng Doanh thu ($)')
axes[0, 2].set_title('Doanh thu theo Kênh Mua hàng')
axes[0, 2].invert_yaxis()

# 4. Phân bố Thời điểm Mua hàng
so_luong_thoi_gian = df['Time_of_Purchase'].value_counts()
mau_thoi_gian = plt.cm.Set3(np.linspace(0, 1, len(so_luong_thoi_gian)))
axes[1, 0].pie(so_luong_thoi_gian.values, labels=so_luong_thoi_gian.index, autopct='%1.1f%%', 
              startangle=90, colors=mau_thoi_gian)
axes[1, 0].set_title('Lượt Mua theo Thời điểm trong ngày')

# 5. Sử dụng Thiết bị
su_dung_thiet_bi = df['Device_Used_for_Shopping'].value_counts()
axes[1, 1].bar(range(len(su_dung_thiet_bi)), su_dung_thiet_bi.values, color='coral', edgecolor='black', alpha=0.7)
axes[1, 1].set_xticks(range(len(su_dung_thiet_bi)))
axes[1, 1].set_xticklabels(su_dung_thiet_bi.index, rotation=45, ha='right')
axes[1, 1].set_ylabel('Số lượt Mua')
axes[1, 1].set_title('Phân bố Sử dụng Thiết bị')

# 6. Tác động của Chương trình Thân thiết
du_lieu_thuong_hieu = pd.DataFrame({
    'Không phải Thành viên': so_sanh_thuong_hieu.loc['Không_phải_Thành_viên'],
    'Thành viên': so_sanh_thuong_hieu.loc['Thành_viên']
})
x = np.arange(len(du_lieu_thuong_hieu.columns))
width = 0.35
cac_chi_so = du_lieu_thuong_hieu.index[:3]
for i, chi_so in enumerate(cac_chi_so):
    axes[1, 2].bar(x + i*width/3, du_lieu_thuong_hieu.loc[chi_so], width/3, label=chi_so)
axes[1, 2].set_ylabel('Giá trị')
axes[1, 2].set_title('Tác động của Chương trình Thân thiết')
axes[1, 2].set_xticks(x + width/3)
axes[1, 2].set_xticklabels(du_lieu_thuong_hieu.columns)
axes[1, 2].legend()

# 7. Mô hình Sử dụng Giảm giá
du_lieu_giam_gia = df['Discount_Used'].value_counts()
mau_giam_gia = ['#FF9999', '#66B2FF']
axes[2, 0].bar(['Không Giảm giá', 'Có Giảm giá'], 
              [du_lieu_giam_gia[False], du_lieu_giam_gia[True]], 
              color=mau_giam_gia, edgecolor='black', alpha=0.7)
axes[2, 0].set_ylabel('Số lượt Mua')
axes[2, 0].set_title('Mô hình Sử dụng Giảm giá')

# 8. Phân khúc Trung thành Thương hiệu
trung_thanh_thuong_hieu = df['Phan_khuc_Trung_thanh'].value_counts()
axes[2, 1].barh(range(len(trung_thanh_thuong_hieu)), trung_thanh_thuong_hieu.values, color='mediumpurple', edgecolor='black')
axes[2, 1].set_yticks(range(len(trung_thanh_thuong_hieu)))
axes[2, 1].set_yticklabels(trung_thanh_thuong_hieu.index)
axes[2, 1].set_xlabel('Số lượng Khách hàng')
axes[2, 1].set_title('Phân khúc Trung thành Thương hiệu')
axes[2, 1].invert_yaxis()

# 9. Tỷ lệ Trả hàng so với Mức độ Hài lòng
bubble = axes[2, 2].scatter(df['Return_Rate'], df['Customer_Satisfaction'], 
                           c=df['Purchase_Amount'], cmap='plasma', alpha=0.6, s=50)
axes[2, 2].set_xlabel('Tỷ lệ Trả hàng (%)')
axes[2, 2].set_ylabel('Mức độ Hài lòng của Khách hàng')
axes[2, 2].set_title('Trả hàng vs Hài lòng (tô màu theo Giá trị)')
thanh_mau = plt.colorbar(bubble, ax=axes[2, 2])
thanh_mau.set_label('Giá trị Đơn hàng ($)')

plt.tight_layout()
plt.savefig('phan_tich_nang_cao.png', dpi=300, bbox_inches='tight')
print("✓ Đã lưu trực quan hóa nâng cao với tên 'phan_tich_nang_cao.png'")
plt.close()

# ================== 11. LƯU BÁO CÁO CHI TIẾT ==================
print("\nĐang lưu các báo cáo phân tích chi tiết...")

# Lưu phân tích rủi ro rời bỏ
bao_cao_rui_ro = df[df['Rui_ro_roi_bo']][['Customer_ID', 'Age', 'Income_Level', 'Purchase_Amount',
                                            'Customer_Satisfaction', 'Location']]
bao_cao_rui_ro.to_csv('khach_hang_rui_ro_roi_bo_cao.csv', index=False)
print("✓ Đã lưu phân tích rủi ro rời bỏ")

# Lưu phân tích CLV
bao_cao_clv = df[['Customer_ID', 'Age', 'Income_Level', 'Purchase_Amount',
                  'Frequency_of_Purchase', 'Customer_Satisfaction', 'CLV_Tiem_nang']].sort_values('CLV_Tiem_nang', ascending=False)
bao_cao_clv.to_csv('gia_tri_vong_doi_khach_hang.csv', index=False)
print("✓ Đã lưu phân tích CLV")

# Lưu hiệu suất kênh
df.groupby('Purchase_Channel').agg({
    'Purchase_Amount': ['mean', 'sum', 'count'],
    'Customer_Satisfaction': 'mean',
    'Return_Rate': 'mean'
}).to_csv('hieu_suat_kenh.csv')
print("✓ Đã lưu hiệu suất kênh")

# Lưu phân tích thiết bị
df.groupby('Device_Used_for_Shopping').agg({
    'Purchase_Amount': ['mean', 'count'],
    'Customer_Satisfaction': 'mean'
}).to_csv('phan_tich_thiet_bi.csv')
print("✓ Đã lưu phân tích thiết bị")

print("\n" + "="*60)
print("PHÂN TÍCH NÂNG CAO HOÀN TẤT!")
print("="*60)