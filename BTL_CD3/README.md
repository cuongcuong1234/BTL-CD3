# E-Commerce Consumer Behavior Analysis - Complete Project Guide

## 📊 Project Overview

This comprehensive analysis project examines e-commerce customer behavior across **1,000 transactions**, providing deep insights into purchasing patterns, customer segmentation, and spending predictions.

**All 5 Required Tasks Completed:**
- ✅ Data Cleaning & Preprocessing
- ✅ Market Basket Analysis (Products Bought Together)
- ✅ Customer Spending Analysis by Segment
- ✅ Consumer Behavior Visualization
- ✅ Customer Spending Prediction Model

---

## 📁 Project Structure

```
BTL_CD3/
├── Main Scripts
│   ├── BaiTap.py                              # Primary analysis & model training
│   ├── AnalysisAdvanced.py                    # Advanced analytics & segmentation
│   ├── GenerateReport.py                      # Comprehensive report generation
│   └── ExecutionSummary.py                    # Analysis summary
│
├── Data Files (Cleaned & Processed)
│   ├── data_cleaned.csv                       # 1,000 cleaned transactions
│   ├── customer_segments_analysis.csv         # 4-cluster segmentation
│   ├── product_combinations.csv               # Market basket analysis (50 pairs)
│   ├── customer_lifetime_value.csv            # CLV rankings
│   ├── high_churn_risk_customers.csv          # 414 at-risk customers
│   ├── model_predictions.csv                  # 200+ spending predictions
│   ├── feature_importance.csv                 # Ranked features
│   ├── channel_performance.csv                # Channel metrics
│   └── device_analysis.csv                    # Device usage analysis
│
├── Visualizations (High-Resolution)
│   ├── consumer_behavior_analysis.png         # 9-panel dashboard (300 DPI)
│   └── advanced_analysis.png                  # 9-panel advanced (300 DPI)
│
└── Reports
    ├── COMPREHENSIVE_ANALYSIS_REPORT.txt      # 500+ line detailed report
    └── ANALYSIS_SUMMARY.txt                   # Executive summary
```

---

## 🚀 Quick Start

### 1. Run All Analyses
```bash
# Run main analysis (data cleaning, segmentation, visualization, prediction)
python BaiTap.py

# Run advanced analytics
python AnalysisAdvanced.py

# Generate comprehensive report
python GenerateReport.py

# View execution summary
python ExecutionSummary.py

📊 PROJECT STATUS: ✅ COMPLETE

All 5 requirements successfully implemented with comprehensive analysis.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 QUICK START - 3 STEPS TO GET INSIGHTS

STEP 1: View Executive Summary
  → Open: COMPREHENSIVE_ANALYSIS_REPORT.txt
  → Read insights, recommendations, findings
  → Time: 15-20 minutes

STEP 2: View Visualizations  
  → Double-click: consumer_behavior_analysis.png
  → Shows: 9-panel overview of all data
  → Time: 5 minutes

STEP 3: Explore Data
  → Open in Excel: data_cleaned.csv (or any .csv file)
  → Drill down into specific segments/customers
  → Time: As needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 KEY FILES EXPLAINED

FOR EXECUTIVES:
  📄 COMPREHENSIVE_ANALYSIS_REPORT.txt    → Full business analysis
  📊 consumer_behavior_analysis.png       → Visual overview
  📊 advanced_analysis.png                → Detailed charts

FOR MARKETING TEAMS:
  🛍️  product_combinations.csv            → Product recommendations
  👥 customer_segments_analysis.csv      → Customer profiles
  ⚠️  high_churn_risk_customers.csv      → Customers at risk

FOR DATA ANALYSTS:
  📈 feature_importance.csv               → Model insights
  📉 model_predictions.csv                → Prediction accuracy
  📊 data_cleaned.csv                     → Full dataset

FOR CHANNEL MANAGERS:
  🌐 channel_performance.csv              → Online/In-Store/Mixed
  📱 device_analysis.csv                  → Desktop/Tablet/Mobile

FOR CUSTOMER SUCCESS:
  💎 customer_lifetime_value.csv          → High-value customers
  ⚠️  high_churn_risk_customers.csv      → At-risk customers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 KEY FINDINGS AT A GLANCE

Transactions Analyzed: 1,000
Total Revenue: $275,063
Average Order: $275

Customer Satisfaction: 5.4/10 ⚠️ BELOW AVERAGE
├─ Need immediate improvement
├─ 41.4% of customers at risk
└─ Segment 2 critical (2.99/10)

Top Products: Electronics, Sports, Home Appliances
Best Channel: Mixed (Online + In-Store)
Best Device: Smartphone ($282 avg)

Churn Risk: 414 customers (41.4%)
Loyalty Members: 491 (49.1%)

4 Customer Segments Identified:
├─ Premium Loyal: 264 (8.22/10 satisfaction) ✅
├─ Young Spenders: 243 (6.24/10)
├─ High-Value Unsatisfied: 253 (2.99/10) ⚠️ 
└─ Budget-Conscious: 240 (3.99/10) ⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 TOP PRIORITY ACTIONS

URGENT (This Week):
  1. ⚠️  Investigate satisfaction crisis (5.4/10)
  2. ⚠️  Contact 414 high-risk customers
  3. ⚠️  Review Segment 2 (253 high-value customers unhappy)

SHORT-TERM (This Month):
  1. Launch quality improvement initiative
  2. Win-back campaigns for at-risk customers
  3. A/B test loyalty program improvements
  4. Optimize top 3 product categories

MEDIUM-TERM (Next Quarter):
  1. Implement personalized product recommendations
  2. Create product bundling strategy
  3. Enhance mobile shopping experience
  4. Launch VIP retention programs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 REQUIREMENT VERIFICATION

✅ 1. LÀMS SẠCH DỮ LIỆU GIAO DỊCH
    • 503 missing values handled
    • Data types converted
    • 99.9% data quality achieved
    → File: data_cleaned.csv

✅ 2. PHÂN TÍCH SẢN PHẨM THƯỜNG MUA CÙNG NHAU  
    • Market basket analysis completed
    • 50 product pairs ranked by frequency
    • Cross-selling opportunities identified
    → File: product_combinations.csv

✅ 3. PHÂN TÍCH CHI TIÊU THEO NHÓM KHÁCH HÀNG
    • 4 customer segments created
    • Spending by income level analyzed
    • Demographics breakdown completed
    → File: customer_segments_analysis.csv

✅ 4. TRỰC QUAN HÓA HÀNH VI TIÊU DÙNG
    • 2 comprehensive dashboards (18 panels)
    • High-resolution (300 DPI)
    • Ready for presentations
    → Files: consumer_behavior_analysis.png
            advanced_analysis.png

✅ 5. DỰ ĐOÁN CHI TIÊU KHÁCH HÀNG
    • Random Forest model trained
    • 28 features analyzed
    • Predictions generated for 200+ samples
    → Files: model_predictions.csv
            feature_importance.csv

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 HOW TO RE-RUN ANALYSIS

All Scripts (Complete Analysis):
  python BaiTap.py
  python AnalysisAdvanced.py
  python GenerateReport.py

Individual Components:
  - BaiTap.py: Data cleaning + segmentation + prediction
  - AnalysisAdvanced.py: Advanced visualizations
  - GenerateReport.py: Comprehensive report

Output: All CSV files, PNG images, and reports regenerated

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ QUICK Q&A

Q: Where do I start?
A: Read COMPREHENSIVE_ANALYSIS_REPORT.txt first (20 min), then view visualizations

Q: Which customers need immediate attention?
A: Use high_churn_risk_customers.csv - these 414 people have satisfaction ≤ 4.0

Q: How accurate are the spending predictions?
A: Test accuracy is -2.7% R² (negative indicates model needs improvement)
   This suggests customer behavior driven by factors beyond available data

Q: Which customer segment is most valuable?
A: Segment 1 (Young High-Spenders) - 243 customers spending $307.94 avg
   BUT Segment 2 (High-Value Unsatisfied) has even higher spending ($330) 
   but very low satisfaction (2.99/10) - convert these and revenue explodes

Q: Should we focus on online or in-store?
A: Mixed channel performs best ($95,164 total), but all channels similar
   Recommendation: Emphasize omnichannel experience

Q: Why is loyalty program showing negative ROI?
A: Program spends on incentives exceed additional revenue generated
   Need: Redesign benefits to better match customer preferences

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 FILE SUMMARY TABLE

File Name                               Type    Purpose                   Size
──────────────────────────────────────  ──────  ───────────────────────   ─────
COMPREHENSIVE_ANALYSIS_REPORT.txt       Report  Full business analysis    500+ lines
ANALYSIS_SUMMARY.txt                    Report  Executive summary         ~300 lines
README.md                               Doc     Project documentation     ~400 lines

data_cleaned.csv                        Data    1000 cleaned transactions 28 cols
customer_segments_analysis.csv          Analysis 4 segments metrics      4 rows
product_combinations.csv                Analysis Top 50 product pairs    50 rows
customer_lifetime_value.csv             Analysis CLV rankings           1000 rows
high_churn_risk_customers.csv           Analysis 414 at-risk customers  414 rows
model_predictions.csv                   Analysis Spending predictions    200 rows
feature_importance.csv                  Analysis 28 ranked features     28 rows
channel_performance.csv                 Analysis 3 channels analyzed    3 rows
device_analysis.csv                     Analysis 3 devices analyzed     3 rows

consumer_behavior_analysis.png          Visual  9-panel dashboard        300 DPI
advanced_analysis.png                   Visual  9-panel advanced         300 DPI

BaiTap.py                               Script  Main analysis            ~500 lines
AnalysisAdvanced.py                     Script  Advanced analytics       ~300 lines
GenerateReport.py                       Script  Report generation        ~500 lines
ExecutionSummary.py                     Script  Summary generation       ~400 lines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ COMPLETION CHECKLIST

Data Preparation:
  ✓ Loaded 1,000 transactions
  ✓ Handled 503 missing values
  ✓ Converted data types
  ✓ Removed duplicates
  ✓ Created clean dataset

Analysis:
  ✓ Exploratory data analysis
  ✓ Customer segmentation (K-means)
  ✓ Market basket analysis
  ✓ Customer profiling
  ✓ Churn risk analysis

Modeling:
  ✓ Random Forest trained (100 estimators)
  ✓ Feature importance calculated
  ✓ Predictions generated
  ✓ Model evaluation completed

Visualization:
  ✓ 18 individual charts created
  ✓ 2 comprehensive dashboards
  ✓ High-resolution (300 DPI)
  ✓ Print-ready format

Reporting:
  ✓ Comprehensive report (500+ lines)
  ✓ Executive summary
  ✓ Strategic recommendations
  ✓ Actionable insights

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 LEARNING RESOURCES

To understand the analysis better:
  - Read COMPREHENSIVE_ANALYSIS_REPORT.txt for business context
  - Review README.md for technical details
  - Check individual CSV files for raw insights
  - View PNG visualizations for quick understanding

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 PROJECT INFORMATION

Project: E-Commerce Consumer Behavior Analysis
Dataset: 1,000 customer transactions
Features: 28 variables (demographic, behavioral, transactional)
Status: ✅ COMPLETE & READY FOR BUSINESS USE
Generated: April 13, 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 NEXT STEPS

1. Review COMPREHENSIVE_ANALYSIS_REPORT.txt (15-20 min)
2. Present visualizations to stakeholders (5 min)
3. Implement immediate priority actions (this week)
4. Schedule monthly analysis reviews (ongoing)
5. Monitor KPIs from strategic recommendations

```

### 2. View Results
- **Quick Visual Overview**: Open `consumer_behavior_analysis.png`
- **Detailed Analysis**: Open `COMPREHENSIVE_ANALYSIS_REPORT.txt`
- **Advanced Charts**: Open `advanced_analysis.png`
- **Data Exploration**: Load any `.csv` file in Excel or Pandas

---

## 📈 Key Findings

### Customer Overview
| Metric | Value |
|--------|-------|
| Total Transactions | 1,000 |
| Total Revenue | $275,063 |
| Average Order Value | $275.06 |
| Average Satisfaction | 5.40/10 ⚠️ |
| Customer Lifetime Value | $1,271 (avg) |

### Customer Demographics
- **Age**: 18-50 years (avg: 34.3)
- **Gender**: Balanced distribution
- **Income**: 51.5% High, 48.5% Middle
- **Top Location**: Varied across regions

### Customer Segments (4 Clusters)

**Segment 0: Premium Loyal Customers** (264 customers)
- Avg Spending: $264.40
- Satisfaction: 8.22/10 ✅
- Loyalty: HIGH
- Strategy: Retention & VIP programs

**Segment 1: Young High-Spenders** (243 customers)
- Avg Spending: $307.94
- Satisfaction: 6.24/10
- Age: 25.2 years (youngest)
- Strategy: Engagement & upselling

**Segment 2: High-Value Unsatisfied** (253 customers)
- Avg Spending: $330.32 (highest)
- Satisfaction: 2.99/10 ⚠️ CRITICAL
- Strategy: Immediate intervention needed

**Segment 3: Budget-Conscious** (240 customers)
- Avg Spending: $195.26 (lowest)
- Satisfaction: 3.99/10 ⚠️
- Age: 40.6 years (oldest)
- Strategy: Value offerings & promotions

### Churn Risk Analysis
- **High-Risk Customers**: 414 (41.4%)
- **Low-Risk Customers**: 586 (58.6%)
- **Satisfaction Threshold**: ≤ 4.0 = High Risk

### Channel Performance
| Channel | Transactions | Revenue | Avg Order | Satisfaction |
|---------|-------------|---------|-----------|--------------|
| Mixed | 340 | $95,164 | $279.90 | 5.46/10 |
| Online | 333 | $91,604 | $274.26 | 5.36/10 |
| In-Store | 327 | $88,295 | $270.84 | 5.46/10 |

### Top Products
1. **Electronics** - 54 purchases (5.4%)
2. **Sports & Outdoors** - 51 purchases (5.1%)
3. **Home Appliances** - 50 purchases (5.0%)
4. **Jewelry & Accessories** - 50 purchases (5.0%)
5. **Toys & Games** - 47 purchases (4.7%)

### Device Usage
- **Desktop**: 31.1% - Avg spending: $266.70
- **Tablet**: 34.5% - Avg spending: $277.29
- **Smartphone**: 34.4% - Avg spending: $282.05 (highest)

---

## 🤖 Predictive Model (Spending Prediction)

### Model Details
- **Type**: Random Forest Regressor
- **Features**: 28 input variables
- **Training Samples**: 800 (80%)
- **Test Samples**: 200 (20%)

### Performance Metrics
```
Training Metrics:
├─ RMSE: $50.68
├─ MAE: $43.13
└─ R²: 0.8510

Test Metrics:
├─ RMSE: $133.73
├─ MAE: $115.54
├─ R²: -0.0270
└─ Avg Error: 24.2%
```

### Top Predictive Features
1. **Location** (13.13%) - Where customer is located
2. **Time of Purchase** (12.94%) - When they buy
3. **Age** (9.46%) - Customer age
4. **Time to Decision** (6.53%) - Decision speed
5. **Purchase Frequency** (6.40%) - Buying frequency

### Sample Predictions
```
Actual: $491.92  →  Predicted: $231.83  (Error: 52.9%)
Actual: $361.27  →  Predicted: $287.83  (Error: 20.3%)
Actual: $442.15  →  Predicted: $311.76  (Error: 29.5%)
Actual: $324.41  →  Predicted: $285.42  (Error: 12.0%)
Actual: $182.94  →  Predicted: $274.39  (Error: 50.0%)
```

---

## 📊 How to Use the Analysis

### 1. For Business Strategy
📄 **Read**: `COMPREHENSIVE_ANALYSIS_REPORT.txt`
- Executive summary
- Strategic recommendations
- Actionable insights

### 2. For Customer Targeting
📊 **Use**: `high_churn_risk_customers.csv`
- Launch retention campaigns for 414 at-risk customers
- Personalized offers & incentives
- Priority customer service

### 3. For Sales Optimization
📈 **Use**: `customer_lifetime_value.csv`
- Identify top-tier customers
- Implement VIP programs
- Focus resources on high-CLV segments

### 4. For Product Bundling
🛍️ **Use**: `product_combinations.csv`
- Cross-sell recommendations
- Bundle deals & promotions
- Strategic product placement

### 5. For Channel Optimization
📱 **Use**: `channel_performance.csv` & `device_analysis.csv`
- Allocate marketing budget
- Optimize mobile experience
- Channel-specific campaigns

### 6. For Model Improvement
🔍 **Use**: `feature_importance.csv`
- Guide future feature engineering
- Focus data collection efforts
- Improve prediction accuracy

---

## 💡 Strategic Recommendations

### Immediate Actions (1-3 months)
- [ ] **Satisfaction Crisis**: Launch quality improvement initiative (target: 7.0/10)
- [ ] **Churn Prevention**: Win-back campaigns for 414 high-risk customers
- [ ] **Loyalty Redesign**: Fix loyalty program (currently -9.4% negative impact)
- [ ] **Top Categories**: Optimize Electronics, Sports, Home Appliances

### Medium-Term (3-6 months)
- [ ] **Personalization**: Implement recommendation engine
- [ ] **Cross-Selling**: Launch product bundling strategy
- [ ] **Mobile**: Enhance smartphone shopping experience
- [ ] **VIP Program**: Create retention programs for top-tier customers

### Long-Term (6-12 months)
- [ ] **Automation**: Implement churn prediction system
- [ ] **AI Integration**: Deploy AI-powered personalization
- [ ] **Market Expansion**: Target middle-income segment
- [ ] **Dynamic Pricing**: Implement segment-based pricing

---

## 🔧 Technical Details

### Requirements
```
Python 3.13+
pandas >= 1.0
numpy >= 1.0
matplotlib >= 3.0
seaborn >= 0.11
scikit-learn >= 0.24
```

### Installation
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Data Processing Pipeline
```
Raw Data (1,000 rows)
    ↓
[Cleaning] - Handle missing values, convert types
    ↓
Clean Data (1,000 rows, 99.9% complete)
    ↓
[Analysis] - Exploratory data analysis
    ↓
[Segmentation] - 4-cluster K-means
    ↓
[Prediction] - Random Forest model training
    ↓
[Visualization] - Create dashboards & charts
    ↓
Results & Insights
```

---

## 📱 File Descriptions

### Data Files

**data_cleaned.csv**
- 1,000 customer transactions
- 28 features (demographic, behavioral, transactional)
- Ready for analysis/modeling
- Contains customer segments (0-3)

**customer_segments_analysis.csv**
- 4 customer clusters with metrics
- Avg spending, frequency, satisfaction per segment
- Use for marketing strategy

**product_combinations.csv**
- Top 50 product pair combinations
- Purchase frequency for each pair
- Use for cross-selling strategy

**customer_lifetime_value.csv**
- All customers ranked by CLV
- Top customers identified
- Includes CLV calculation details

**high_churn_risk_customers.csv**
- 414 customers with satisfaction ≤ 4.0
- Demographics and spending patterns
- Priority targets for retention

**model_predictions.csv**
- 200 test set predictions vs actual
- Prediction errors and percentages
- Evaluate model performance

**feature_importance.csv**
- 28 features ranked by importance
- Contribution to spending prediction
- Guide for future modeling

### Visualization Files

**consumer_behavior_analysis.png**
- 9-panel comprehensive dashboard
- Distributions, categories, channels
- Ready for stakeholder presentations

**advanced_analysis.png**
- 9-panel advanced analytics
- CLV, churn risk, loyalty analysis
- Detailed insights visualization

---

## ❓ FAQ

**Q: Why is customer satisfaction only 5.4/10?**
A: Review `COMPREHENSIVE_ANALYSIS_REPORT.txt` - this is a critical finding requiring immediate investigation into product quality and customer service.

**Q: How should I use the churn risk file?**
A: The 414 high-risk customers should receive personalized retention campaigns - special offers, surveys to understand issues, and priority service improvements.

**Q: Why are predictions less accurate on test data?**
A: Customer spending is influenced by many factors beyond the collected features. Consider adding seasonal data, marketing spend, product availability, and competitor pricing.

**Q: Which segment should we focus on?**
A: Prioritize Segment 2 (high-value unsatisfied) - high spending but low satisfaction. Improving their experience could significantly boost revenue.

**Q: How often should we update this analysis?**
A: Run monthly to track trends, detect satisfaction changes, and monitor retention initiatives effectiveness.

---

## 📞 Support & Questions

For detailed insights, refer to these files in order:
1. `ANALYSIS_SUMMARY.txt` - Quick overview
2. `COMPREHENSIVE_ANALYSIS_REPORT.txt` - Full analysis
3. Individual CSV files - Detailed data exploration
4. PNG visualizations - Executive presentations

---

## 📋 Deliverables Checklist

✅ **Requirement 1: Data Cleaning**
- Missing values: 503 handled
- Data types: Converted
- Result: 99.9% data quality

✅ **Requirement 2: Market Basket Analysis**
- Product pairs: 50 analyzed
- Cross-selling insights: Generated
- Output: product_combinations.csv

✅ **Requirement 3: Spending by Customer Group**
- Segments: 4 clusters identified
- By income level: High vs Middle analyzed
- By demographics: Gender, age, location
- Output: customer_segments_analysis.csv

✅ **Requirement 4: Consumer Behavior Visualization**
- Dashboards: 2 comprehensive (18 panels total)
- Resolution: 300 DPI (print-ready)
- Files: consumer_behavior_analysis.png, advanced_analysis.png

✅ **Requirement 5: Spending Prediction**
- Model: Random Forest (100 estimators)
- Features: 28 input variables
- Predictions: 200+ samples
- Performance: -2.7% R² (documented)
- Output: model_predictions.csv, feature_importance.csv

---

**Report Generated**: April 13, 2026  
**Analysis Period**: Complete e-commerce dataset  
**Data Quality**: 99.9% complete  
**Status**: ✅ READY FOR BUSINESS IMPLEMENTATION

---
