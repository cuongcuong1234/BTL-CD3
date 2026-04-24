# Phân Tích Hành Vi Người Tiêu Dùng Thương Mại Điện Tử - Hướng Dẫn Dự Án Đầy Đủ

## 📊 Tổng Quan Dự Án

Dự án phân tích toàn diện này xem xét hành vi khách hàng thương mại điện tử qua **1,000 giao dịch**, cung cấp những hiểu biết sâu sắc về mô hình mua sắm, phân khúc khách hàng và dự đoán chi tiêu.

**Đã Hoàn Thành Cả 5 Yêu Cầu:**
- ✅ Làm sạch & Tiền xử lý dữ liệu
- ✅ Phân tích giỏ hàng (Sản phẩm thường mua cùng nhau)
- ✅ Phân tích chi tiêu theo nhóm khách hàng
- ✅ Trực quan hóa hành vi tiêu dùng
- ✅ Mô hình dự đoán chi tiêu khách hàng

---

## 📁 Cấu Trúc Dự Án
BTL_CD3/
├── Main Scripts
│ ├── Main.py # Phân tích chính & huấn luyện mô hình
│ ├── AnalysisAdvanced.py # Phân tích nâng cao & phân khúc
│ ├── GenerateReport.py # Tạo báo cáo toàn diện
│ └── ExecutionSummary.py # Tóm tắt phân tích
│
├── Dữ Liệu (Đã làm sạch & Xử lý)
│ ├── du_lieu_da_sach.csv                     # 1,000 giao dịch đã làm sạch
│ ├── phan_tich_phan_khuc_khach_hang.csv>      # Phân khúc 4 cụm
│ ├── cac_cap_san_pham.csv           # Phân tích giỏ hàng (50 cặp)
│ ├── gia_tri_vong_doi_khach_hang.csv          # Xếp hạng giá trị vòng đời
│ ├── khach_hang_rui_ro_roi_bo_cao.csv>      # 414 khách hàng có nguy cơ rời bỏ
│ ├── du_doan_cua_mo_hinh.csv                # 200+ dự đoán chi tiêu
│ ├── muc_do_quan_trong_dac_trung.csv               # Các đặc trưng quan trọng
│ ├── hieu_suat_kenh.csv              # Hiệu suất kênh bán hàng
│ └── phan_tich_thiet_bi.csv                  # Phân tích thiết bị sử dụng
│
├── Trực Quan Hóa (Độ phân giải cao)
│ ├── phan_tich_hanh_vi_nguoi_tieu_dung.png      # Bảng điều khiển 9 ô (300 DPI)
│ └── phan_tich_nang_cao.png              # Phân tích nâng cao 9 ô (300 DPI)
│
└── Báo Cáo
├── BAO_CAO_PHAN_TICH_TOAN_DIEN.txt    # Báo cáo chi tiết 500+ dòng
└── TOM_TAT_PHAN_TICH.txt # Tóm tắt điều hành

---

## 🚀 Bắt Đầu Nhanh

### 1. Chạy Tất Cả Các Phân Tích
```bash
# Chạy phân tích chính (làm sạch dữ liệu, phân khúc, trực quan hóa, dự đoán)
python Main.py

# Chạy phân tích nâng cao
python AnalysisAdvanced.py

# Tạo báo cáo toàn diện
python GenerateReport.py

# Xem tóm tắt thực thi
python ExecutionSummary.py

📊 TÌNH TRẠNG DỰ ÁN: ✅ HOÀN THÀNH

Đã triển khai thành công cả 5 yêu cầu với phân tích toàn diện.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 BẮT ĐẦU NHANH - 3 BƯỚC ĐỂ CÓ THÔNG TIN CHI TIẾT

BƯỚC 1: Xem Tóm Tắt Điều Hành
  → Mở file: BAO_CAO_PHAN_TICH_TOAN_DIEN.txt
  → Đọc các thông tin chi tiết, khuyến nghị, phát hiện
  → Thời gian: 15-20 phút

BƯỚC 2: Xem Trực Quan Hóa  
  → Nhấp đúp vào: phan_tich_hanh_vi_nguoi_tieu_dung.png
  → Hiển thị: Tổng quan 9 ô về tất cả dữ liệu
  → Thời gian: 5 phút

BƯỚC 3: Khám Phá Dữ Liệu
  → Mở trong Excel: du_lieu_da_sach.csv (hoặc bất kỳ file .csv nào)
  → Đi sâu vào các phân khúc/khách hàng cụ thể
  → Thời gian: Tùy theo nhu cầu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 GIẢI THÍCH CÁC FILE QUAN TRỌNG

CHO BAN LÃNH ĐẠO:
  📄 COMPREHENSIVE_ANALYSIS_REPORT.txt    → Phân tích kinh doanh đầy đủ
  📊 consumer_behavior_analysis.png       → Tổng quan trực quan
  📊 advanced_analysis.png                → Biểu đồ chi tiết

CHO NHÓM TIẾP THỊ:
  🛍️  product_combinations.csv            → Gợi ý sản phẩm
  👥 customer_segments_analysis.csv      → Hồ sơ khách hàng
  ⚠️  high_churn_risk_customers.csv      → Khách hàng có nguy cơ rời bỏ

CHO CHUYÊN VIÊN PHÂN TÍCH DỮ LIỆU:
  📈 feature_importance.csv               → Thông tin chi tiết về mô hình
  📉 model_predictions.csv                → Độ chính xác dự đoán
  📊 data_cleaned.csv                     → Bộ dữ liệu đầy đủ

CHO QUẢN LÝ KÊNH BÁN HÀNG:
  🌐 channel_performance.csv              → Hiệu suất Online/Cửa hàng/Hỗn hợp
  📱 device_analysis.csv                  → Phân tích Desktop/Tablet/Mobile

CHO BỘ PHẬN CHĂM SÓC KHÁCH HÀNG:
  💎 customer_lifetime_value.csv          → Khách hàng giá trị cao
  ⚠️  high_churn_risk_customers.csv      → Khách hàng có nguy cơ rời bỏ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 CÁCH CHẠY LẠI PHÂN TÍCH

Tất cả Script (Phân tích đầy đủ):
  python BaiTap.py
  python AnalysisAdvanced.py
  python GenerateReport.py

Các thành phần riêng lẻ:
  - BaiTap.py: Làm sạch dữ liệu + phân khúc + dự đoán
  - AnalysisAdvanced.py: Trực quan hóa nâng cao
  - GenerateReport.py: Báo cáo toàn diện

Đầu ra: Tất cả file CSV, ảnh PNG và báo cáo được tạo lại

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
