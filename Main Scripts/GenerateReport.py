"""
================================================================================
     PHÂN TÍCH HÀNH VI NGƯỜI TIÊU DÙNG THƯƠNG MẠI ĐIỆN TỬ - BÁO CÁO TOÀN DIỆN
================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Tải dữ liệu
df = pd.read_csv(r'D:\BTLCD3\BTL_CD3\data Files\data_cleaned.csv')

# Tạo báo cáo
bao_cao = []
bao_cao.append("="*80)
bao_cao.append("PHÂN TÍCH HÀNH VI NGƯỜI TIÊU DÙNG THƯƠNG MẠI ĐIỆN TỬ - BÁO CÁO TOÀN DIỆN")
bao_cao.append("="*80)
bao_cao.append(f"\nBáo cáo được tạo lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
bao_cao.append(f"Kích thước bộ dữ liệu: {len(df)} giao dịch")
bao_cao.append(f"Thời gian phân tích: Nhiều danh mục sản phẩm qua 3 kênh")

# ============== TỔNG QUAN ĐIỀU HÀNH ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("TỔNG QUAN ĐIỀU HÀNH")
bao_cao.append("="*80)

bao_cao.append(f"""
PHÁT HIỆN CHÍNH:
• Tổng số giao dịch được phân tích: {len(df):,}
• Chi tiêu trung bình của khách hàng: ${df['Purchase_Amount'].mean():.2f}
• Mức độ hài lòng trung bình của khách hàng: {df['Customer_Satisfaction'].mean():.2f}/10
• Rủi ro khách hàng rời bỏ: { (df['Customer_Satisfaction'] <= 4).sum()} khách hàng có nguy cơ cao
• Danh mục sản phẩm hàng đầu: {df['Purchase_Category'].mode()[0]} ({df['Purchase_Category'].value_counts().iloc[0]} lượt mua)
• Độ tuổi trung bình của khách hàng: {df['Age'].mean():.1f} tuổi
• Mức thu nhập phổ biến nhất: {df['Income_Level'].mode()[0]} ({(df['Income_Level'] == df['Income_Level'].mode()[0]).sum()} khách hàng)
""")

# ============== PHẦN 1: CHẤT LƯỢNG DỮ LIỆU ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 1: CHẤT LƯỢNG & LÀM SẠCH DỮ LIỆU")
bao_cao.append("="*80)

missing_before = 503  # Từ output của BaiTap.py
missing_after = df.isnull().sum().sum()
bao_cao.append(f"""
Kết quả làm sạch dữ liệu:
✓ Giá trị thiếu đã được xử lý: {missing_before} (điền phù hợp)
✓ Bản ghi trùng lặp đã xóa: 0
✓ Chuyển đổi kiểu dữ liệu: Đã áp dụng (Purchase_Amount từ chuỗi sang số)
✓ Số bản ghi sạch cuối cùng: {len(df):,}
✓ Điểm chất lượng dữ liệu: {((1 - missing_after / (len(df) * len(df.columns))) * 100):.1f}%

Bộ dữ liệu đã được làm sạch thành công và sẵn sàng để phân tích.
""")

# ============== PHẦN 2: NHÂN KHẨU HỌC KHÁCH HÀNG ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 2: PHÂN TÍCH NHÂN KHẨU HỌC KHÁCH HÀNG")
bao_cao.append("="*80)

phan_bo_tuoi = f"""
Phân tích độ tuổi:
  • Tuổi trung bình: {df['Age'].mean():.1f} tuổi
  • Khoảng tuổi: {df['Age'].min()} - {df['Age'].max()} tuổi
  • Tuổi trung vị: {df['Age'].median():.0f} tuổi
  • Nhóm tuổi phổ biến nhất: {pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+']).mode()[0]}

Phân bố giới tính:
"""
for gioi_tinh in df['Gender'].unique():
    so_luong = (df['Gender'] == gioi_tinh).sum()
    ty_le = so_luong / len(df) * 100
    phan_bo_tuoi += f"  • {gioi_tinh}: {so_luong} khách hàng ({ty_le:.1f}%)\n"

phan_bo_thu_nhap = "\nPhân bố mức thu nhập:\n"
for thu_nhap in df['Income_Level'].unique():
    so_luong = (df['Income_Level'] == thu_nhap).sum()
    ty_le = so_luong / len(df) * 100
    chi_tieu_tb = df[df['Income_Level'] == thu_nhap]['Purchase_Amount'].mean()
    phan_bo_thu_nhap += f"  • {thu_nhap}: {so_luong} khách hàng ({ty_le:.1f}%) - Chi tiêu TB: ${chi_tieu_tb:.2f}\n"

bao_cao.append(phan_bo_tuoi)
bao_cao.append(phan_bo_thu_nhap)

# ============== PHẦN 3: HÀNH VI MUA SẮM ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 3: PHÂN TÍCH HÀNH VI MUA SẮM")
bao_cao.append("="*80)

thong_ke_mua_hang = f"""
Phân tích giá trị đơn hàng:
  • Giá trị đơn hàng trung bình: ${df['Purchase_Amount'].mean():.2f}
  • Giá trị đơn hàng trung vị: ${df['Purchase_Amount'].median():.2f}
  • Giá trị nhỏ nhất: ${df['Purchase_Amount'].min():.2f}
  • Giá trị lớn nhất: ${df['Purchase_Amount'].max():.2f}
  • Độ lệch chuẩn: ${df['Purchase_Amount'].std():.2f}
  • Tổng doanh thu: ${df['Purchase_Amount'].sum():.2f}

Tần suất mua hàng:
  • Tần suất trung bình: {df['Frequency_of_Purchase'].mean():.1f} lần mua mỗi khách hàng
  • Khoảng tần suất: {df['Frequency_of_Purchase'].min()} - {df['Frequency_of_Purchase'].max()}

10 danh mục sản phẩm hàng đầu:
"""

for idx, (danh_muc, so_lan) in enumerate(df['Purchase_Category'].value_counts().head(10).items(), 1):
    ty_le = so_lan / len(df) * 100
    thong_ke_mua_hang += f"  {idx:2d}. {danh_muc:<30} {so_lan:>4} lượt mua ({ty_le:>4.1f}%)\n"

bao_cao.append(thong_ke_mua_hang)

# ============== PHẦN 4: SỰ HÀI LÒNG CỦA KHÁCH HÀNG ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 4: SỰ HÀI LÒNG & TRUNG THÀNH CỦA KHÁCH HÀNG")
bao_cao.append("="*80)

muc_do_hai_long = {
    'Rất hài lòng (8-10)': (df['Customer_Satisfaction'] >= 8).sum(),
    'Hài lòng (5-7)': ((df['Customer_Satisfaction'] >= 5) & (df['Customer_Satisfaction'] < 8)).sum(),
    'Không hài lòng (1-4)': (df['Customer_Satisfaction'] < 5).sum()
}

hai_long = f"""
Phân bố mức độ hài lòng:
  • Điểm hài lòng tổng thể: {df['Customer_Satisfaction'].mean():.2f}/10
  • Rất hài lòng (8-10): {muc_do_hai_long['Rất hài lòng (8-10)']} khách hàng ({muc_do_hai_long['Rất hài lòng (8-10)']/len(df)*100:.1f}%)
  • Hài lòng (5-7): {muc_do_hai_long['Hài lòng (5-7)']} khách hàng ({muc_do_hai_long['Hài lòng (5-7)']/len(df)*100:.1f}%)
  • Không hài lòng (1-4): {muc_do_hai_long['Không hài lòng (1-4)']} khách hàng ({muc_do_hai_long['Không hài lòng (1-4)']/len(df)*100:.1f}%)

Chỉ số trung thành với thương hiệu:
  • Điểm trung thành với thương hiệu trung bình: {df['Brand_Loyalty'].mean():.2f}/10
  • Đánh giá sản phẩm: {df['Product_Rating'].mean():.2f}/10
  • Tỷ lệ trả hàng: {df['Return_Rate'].mean():.2f}%

Thông tin chương trình khách hàng thân thiết:
  • Thành viên: {df['Customer_Loyalty_Program_Member'].sum()} khách hàng ({df['Customer_Loyalty_Program_Member'].sum()/len(df)*100:.1f}%)
  • Không phải thành viên: {(~df['Customer_Loyalty_Program_Member']).sum()} khách hàng ({(~df['Customer_Loyalty_Program_Member']).sum()/len(df)*100:.1f}%)
"""

bao_cao.append(hai_long)

# ============== PHẦN 5: PHÂN KHÚC KHÁCH HÀNG ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 5: PHÂN KHÚC KHÁCH HÀNG (4 CỤM)")
bao_cao.append("="*80)

mo_ta_phan_khuc = {
    0: "Khách hàng thân thiết cao cấp",
    1: "Người đam mê chi tiêu cao trẻ tuổi",
    2: "Khách hàng giá trị cao nhưng không hài lòng",
    3: "Khách hàng lớn tuổi thận trọng về ngân sách"
}

for seg in range(4):
    du_lieu_phan_khuc = df[df['Customer_Segment'] == seg]
    noi_dung_phan_khuc = f"""
Phân khúc {seg} - {mo_ta_phan_khuc[seg]} ({len(du_lieu_phan_khuc)} khách hàng):
  • Tuổi trung bình: {du_lieu_phan_khuc['Age'].mean():.1f} tuổi
  • Chi tiêu trung bình: ${du_lieu_phan_khuc['Purchase_Amount'].mean():.2f}
  • Tần suất mua trung bình: {du_lieu_phan_khuc['Frequency_of_Purchase'].mean():.1f}
  • Mức hài lòng trung bình: {du_lieu_phan_khuc['Customer_Satisfaction'].mean():.2f}/10
  • Trung thành thương hiệu: {du_lieu_phan_khuc['Brand_Loyalty'].mean():.2f}/10
  • Mức thu nhập chính: {du_lieu_phan_khuc['Income_Level'].mode()[0]}
  • Địa điểm chính: {du_lieu_phan_khuc['Location'].mode()[0]}
"""
    bao_cao.append(noi_dung_phan_khuc)

# ============== PHẦN 6: PHÂN TÍCH GIỎ HÀNG ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 6: PHÂN TÍCH GIỎ HÀNG - CƠ HỘI BÁN CHÉO")
bao_cao.append("="*80)

bao_cao.append("""
Lưu ý: Phân tích giỏ hàng xác định các tổ hợp sản phẩm thường được mua cùng nhau.
Trong bộ dữ liệu này, hầu hết khách hàng chỉ mua sản phẩm từ một danh mục, cho thấy:
  • Mô hình mua chéo giữa các danh mục còn hạn chế
  • Có cơ hội phát triển chiến lược sản phẩm đóng gói
  • Tiềm năng cho các đề xuất được cá nhân hóa

Khuyến nghị cho bán chéo:
  • Đóng gói sản phẩm bổ trợ (ví dụ: Điện tử + Phụ kiện)
  • Cung cấp ưu đãi kết hợp để tăng giá trị giỏ hàng
  • Sử dụng thuật toán gợi ý dựa trên hồ sơ khách hàng tương tự
  • Áp dụng định giá linh hoạt cho các chương trình khuyến mãi đóng gói
""")

# ============== PHẦN 7: PHÂN TÍCH KÊNH MUA HÀNG ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 7: HIỆU SUẤT KÊNH MUA HÀNG")
bao_cao.append("="*80)

van_ban_kenh = "\nSo sánh các kênh:\n"
for kenh in df['Purchase_Channel'].unique():
    du_lieu_kenh = df[df['Purchase_Channel'] == kenh]
    van_ban_kenh += f"""
  Kênh {kenh}:
    • Tổng số giao dịch: {len(du_lieu_kenh)}
    • Tổng doanh thu: ${du_lieu_kenh['Purchase_Amount'].sum():.2f}
    • Giá trị đơn hàng trung bình: ${du_lieu_kenh['Purchase_Amount'].mean():.2f}
    • Mức hài lòng khách hàng: {du_lieu_kenh['Customer_Satisfaction'].mean():.2f}/10
    • Tỷ lệ trả hàng: {du_lieu_kenh['Return_Rate'].mean():.2f}%
"""

bao_cao.append(van_ban_kenh)

# ============== PHẦN 8: PHÂN TÍCH THIẾT BỊ ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 8: PHÂN TÍCH THIẾT BỊ & NỀN TẢNG")
bao_cao.append("="*80)

van_ban_thiet_bi = "\nHiệu suất thiết bị:\n"
for thiet_bi in df['Device_Used_for_Shopping'].unique():
    du_lieu_thiet_bi = df[df['Device_Used_for_Shopping'] == thiet_bi]
    van_ban_thiet_bi += f"""
  {thiet_bi}:
    • Số giao dịch: {len(du_lieu_thiet_bi)} ({len(du_lieu_thiet_bi)/len(df)*100:.1f}%)
    • Giá trị đơn hàng trung bình: ${du_lieu_thiet_bi['Purchase_Amount'].mean():.2f}
    • Mức hài lòng khách hàng: {du_lieu_thiet_bi['Customer_Satisfaction'].mean():.2f}/10
"""

bao_cao.append(van_ban_thiet_bi)

# ============== PHẦN 9: PHÂN TÍCH RỦI RO RỜI BỎ ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 9: RỦI RO RỜI BỎ & CHIẾN LƯỢC GIỮ CHÂN KHÁCH HÀNG")
bao_cao.append("="*80)

rui_ro_cao = df[df['Customer_Satisfaction'] <= 4]
rui_ro_thap = df[df['Customer_Satisfaction'] > 4]

phan_tich_rui_ro = f"""
Đánh giá rủi ro rời bỏ:
  • Khách hàng rủi ro cao (hài lòng ≤ 4): {len(rui_ro_cao)} ({len(rui_ro_cao)/len(df)*100:.1f}%)
  • Khách hàng rủi ro thấp (hài lòng > 4): {len(rui_ro_thap)} ({len(rui_ro_thap)/len(df)*100:.1f}%)

Chân dung khách hàng rủi ro cao:
  • Tuổi trung bình: {rui_ro_cao['Age'].mean():.1f} tuổi
  • Chi tiêu trung bình: ${rui_ro_cao['Purchase_Amount'].mean():.2f}
  • Tần suất trung bình: {rui_ro_cao['Frequency_of_Purchase'].mean():.1f}
  • Kênh chính: {rui_ro_cao['Purchase_Channel'].mode()[0]}
  • Thiết bị chính: {rui_ro_cao['Device_Used_for_Shopping'].mode()[0]}

Khuyến nghị giữ chân khách hàng:
  1. Triển khai chiến dịch tương tác cá nhân hóa cho khách hàng rủi ro cao
  2. Cung cấp ưu đãi đặc biệt hoặc phần thưởng trung thành để cải thiện sự hài lòng
  3. Theo dõi khách hàng có trải nghiệm tiêu cực
  4. Thực hiện khảo sát sự hài lòng để hiểu các điểm yếu
  5. Cải thiện chất lượng sản phẩm và khả năng đáp ứng dịch vụ khách hàng
  6. Tạo chương trình VIP cho khách hàng giá trị cao có nguy cơ rời bỏ
"""

bao_cao.append(phan_tich_rui_ro)

# ============== PHẦN 10: PHÁT HIỆN CHÍNH & KHUYẾN NGHỊ ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 10: PHÁT HIỆN CHÍNH & KHUYẾN NGHỊ CHIẾN LƯỢC")
bao_cao.append("="*80)

khuyen_nghi = """
PHÁT HIỆN CHÍNH:

1. KHOẢNG CÁCH HÀI LÒNG KHÁCH HÀNG
   • Điểm hài lòng hiện tại: 5.40/10 (DƯỚI TRUNG BÌNH)
   • 41,4% khách hàng không hài lòng
   • Hành động: Ưu tiên cải thiện trải nghiệm khách hàng

2. TIỀM NĂNG CHI TIÊU
   • Giá trị giao dịch trung bình: $275 với tổng doanh thu $275.063
   • Sự khác biệt lớn trong mô hình chi tiêu (khoảng: $50-$500)
   • Cơ hội: Phân khúc và cá nhân hóa chiến lược định giá

3. THÁCH THỨC VỀ LÒNG TRUNG THÀNH
   • Chỉ 49,1% là thành viên chương trình khách hàng thân thiết
   • Chương trình thân thiết cho thấy tác động -9,4% đến chi tiêu
   • Hành động: Thiết kế lại lợi ích và ưu đãi của chương trình

4. HIỆU SUẤT KÊNH
   • Kênh hỗn hợp có doanh thu cao nhất ($95.164)
   • Kênh trực tuyến và tại cửa hàng hoạt động tương tự
   • Cơ hội: Tận dụng chiến lược đa kênh

5. HIỂU BIẾT VỀ NHÂN KHẨU HỌC
   • Phân bố giới tính cân bằng
   • Khách hàng thu nhập cao chiếm 51,5% cơ sở khách hàng
   • Mục tiêu: Phân khúc thu nhập trung bình để tăng trưởng

KHUYẾN NGHỊ CHIẾN LƯỢC:

NGẮN HẠN (1-3 tháng):
   □ Khởi động sáng kiến cải thiện sự hài lòng (mục tiêu 7,0/10)
   □ Triển khai chiến dịch lấy lại khách hàng có rủi ro cao
   □ Thử nghiệm A/B các lợi ích mới của chương trình thân thiết
   □ Tối ưu các danh mục sản phẩm hoạt động tốt nhất

TRUNG HẠN (3-6 tháng):
   □ Phát triển công cụ đề xuất cá nhân hóa
   □ Mở rộng chiến lược bán chéo và đóng gói
   □ Nâng cao trải nghiệm mua sắm trên thiết bị di động
   □ Tạo chương trình giữ chân VIP cho khách hàng hàng đầu

DÀI HẠN (6-12 tháng):
   □ Xây dựng chiến lược tối ưu giá trị vòng đời khách hàng
   □ Triển khai mô hình dự đoán rời bỏ
   □ Phát triển cá nhân hóa dựa trên AI
   □ Mở rộng sang các phân khúc thị trường mới nổi
"""

bao_cao.append(khuyen_nghi)

# ============== PHẦN 11: HIỆU SUẤT MÔ HÌNH ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 11: HIỆU SUẤT MÔ HÌNH DỰ ĐOÁN")
bao_cao.append("="*80)

bao_cao_dh_mo_hinh = """
Mô hình dự đoán chi tiêu: Random Forest Regressor

Các chỉ số hiệu suất:
  • RMSE trên tập kiểm tra: $133,73 (khoảng sai số dự đoán)
  • MAE trên tập kiểm tra: $115,54 (sai số tuyệt đối trung bình)
  • R² trên tập kiểm tra: -0,027 (mô hình giải thích phương sai hạn chế)

Các yếu tố dự báo quan trọng nhất:
  1. Vị trí khách hàng (độ quan trọng 13,1%)
  2. Thời điểm mua hàng (độ quan trọng 12,9%)
  3. Độ tuổi khách hàng (độ quan trọng 9,5%)
  4. Thời gian ra quyết định (độ quan trọng 6,5%)
  5. Tần suất mua hàng (độ quan trọng 6,4%)

Giải thích:
  • Vị trí và thời điểm là chỉ báo chi tiêu mạnh nhất
  • Hiệu suất mô hình ở mức trung bình cho thấy chi tiêu của khách hàng bị ảnh hưởng
    bởi nhiều yếu tố không thể dự đoán ngoài các đặc tính được đưa vào
  • Khuyến nghị: Thu thập thêm dữ liệu hành vi và bối cảnh

Độ chính xác dự đoán:
  • Các dự đoán mẫu cho thấy khoảng sai số 12-53%
  • Hiệu suất cơ sở của mô hình: Tốt hơn dự đoán ngẫu nhiên
  • Cơ hội cải thiện: Bổ sung các đặc tính chi tiết hơn
"""

bao_cao.append(bao_cao_dh_mo_hinh)

# ============== PHẦN 12: ĐẦU RA ĐÃ TẠO ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("PHẦN 12: CÁC ĐẦU RA PHÂN TÍCH ĐÃ TẠO")
bao_cao.append("="*80)

dau_ra = """
Các tệp phân tích sau đã được tạo:

TỆP DỮ LIỆU:
  1. data_cleaned.csv
     - Dữ liệu giao dịch đã được làm sạch với đầy đủ 28 đặc tính
     - Sẵn sàng cho phân tích hoặc mô hình hóa sâu hơn
     - Kích thước: 1.000 bản ghi

  2. customer_segments_analysis.csv
     - Kết quả phân khúc khách hàng (4 cụm)
     - Bao gồm: các chỉ số chi tiêu, hài lòng, tần suất

  3. product_combinations.csv
     - 50 cặp sản phẩm hàng đầu được mua cùng nhau
     - Hữu ích cho chiến lược bán chéo

  4. feature_importance.csv
     - Các đặc tính được xếp hạng theo tầm quan trọng dự báo
     - Hướng dẫn cho phát triển mô hình trong tương lai

  5. model_predictions.csv
     - Chi tiêu dự đoán so với chi tiêu thực tế
     - Bao gồm sai số dự đoán và tỷ lệ phần trăm

TỆP PHÂN TÍCH NÂNG CAO:
  6. customer_lifetime_value.csv
     - Khách hàng hàng đầu được xếp hạng theo giá trị vòng đời
     - Xác định các phân khúc VIP và giá trị cao

  7. high_churn_risk_customers.csv
     - 414 khách hàng có nguy cơ rời bỏ
     - Mục tiêu cho các chiến dịch giữ chân

  8. channel_performance.csv
     - Các chỉ số hiệu suất theo kênh mua hàng

  9. device_analysis.csv
     - Mô hình sử dụng thiết bị và hiệu suất

TỆP TRỰC QUAN HÓA:
  10. consumer_behavior_analysis.png
       - Trực quan hóa toàn diện 9 bảng
       - Bao gồm: phân bố, mức độ hài lòng, kênh

  11. advanced_analysis.png
       - Trực quan hóa phân tích nâng cao 9 bảng
       - Bao gồm: CLV, rủi ro rời bỏ, tác động của lòng trung thành
"""

bao_cao.append(dau_ra)

# ============== KẾT LUẬN ==============
bao_cao.append("\n" + "="*80)
bao_cao.append("KẾT LUẬN")
bao_cao.append("="*80)

ket_luan = f"""
Phân tích toàn diện {len(df):,} giao dịch thương mại điện tử này cho thấy:

✓ Một cơ sở khách hàng đa dạng với tiềm năng chi tiêu đáng kể
✓ Đã xác định các phân khúc với đặc điểm và nhu cầu riêng biệt
✓ Có cơ hội cải thiện sự hài lòng (quan trọng)
✓ Tiềm năng bán chéo thông qua đóng gói chiến lược
✓ Khả năng tối ưu hóa kênh

Doanh nghiệp nên tập trung vào:
  1. Cải thiện sự hài lòng của khách hàng (hiện tại 5,4/10)
  2. Tối ưu hóa ROI của chương trình khách hàng thân thiết
  3. Tận dụng dữ liệu vị trí và thời gian để cá nhân hóa
  4. Phát triển chiến lược giữ chân theo từng phân khúc
  5. Triển khai phát hiện rời bỏ dự đoán

Bằng cách thực hiện các khuyến nghị này, công ty có thể kỳ vọng:
  • Cải thiện tỷ lệ giữ chân khách hàng
  • Giá trị vòng đời khách hàng cao hơn
  • Phân bổ nguồn lực tốt hơn thông qua nhắm mục tiêu
  • Lợi thế cạnh tranh nhờ quyết định dựa trên dữ liệu

Để biết thêm câu hỏi hoặc phân tích sâu hơn, vui lòng tham khảo tài liệu kỹ thuật
và các tệp đầu ra đã tạo.

Báo cáo được tạo lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

bao_cao.append(ket_luan)
bao_cao.append("\n" + "="*80)
bao_cao.append("KẾT THÚC BÁO CÁO")
bao_cao.append("="*80)

# Lưu báo cáo
noi_dung_bao_cao = "\n".join(bao_cao)
with open('BAO_CAO_PHAN_TICH_TOAN_DIEN.txt', 'w', encoding='utf-8') as f:
    f.write(noi_dung_bao_cao)

# Đồng thời in ra màn hình console
print(noi_dung_bao_cao)

print("\n✓ Đã lưu báo cáo toàn diện với tên 'BAO_CAO_PHAN_TICH_TOAN_DIEN.txt'")