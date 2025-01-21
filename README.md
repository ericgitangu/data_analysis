# Kwanza Tukule Data Analysis Assessment 🥗📊

[![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
[![Python Tests](https://img.shields.io/badge/pytest-passing-brightgreen)](https://github.com/your-username/kwanza-tukule-analysis/actions)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/your-username/kwanza-tukule-analysis/issues)


>This project performs a comprehensive analysis of the Kwanza Tukule dataset, including data cleaning, exploration, advanced analytics, strategic recommendations, and an interactive dashboard. The results and insights are saved both to the **console and to files** for easy access. Also note for plots generated, you need to close the current chart (Matplotlib) to proceed with execution and watch out for the interactive dashboards (Total Value by Category) & (Sales Trends Over Time) with both open on localhost using plotly.

---

## 📚 Features

- **Section 1: Data Cleaning and Preparation**
  - Inspects the dataset for missing values, duplicates, and inconsistent data types.
  - Creates a `Month-Year` column for temporal analysis.

- **Section 2: Exploratory Data Analysis**
  - Aggregates sales by category and business.
  - Visualizes trends over time with bar and line charts.

- **Section 3: Advanced Analysis**
  - Segments customers based on purchasing behavior.
  - Provides insights into high-, medium-, and low-value customer groups.

- **Section 4: Strategic Insights and Recommendations**
  - Outputs recommendations for product strategy, customer retention, and operational efficiency.
  - Saves recommendations to a file for reporting.

- **Section 5: Dashboard and Reporting**
  - Generates an interactive dashboard with:
    - Total Quantity and Value by Anonymized Category.
    - Top-performing products and businesses.
    - A time-series chart of sales trends.
    - A segmentation summary of customer groups.
  - Built using `plotly` for interactivity.

- **Bonus Section: Open-Ended Problem**
  - Discusses scalability and predictive analysis methodologies.
  - Saves responses to a file for documentation.

---

## 🚀 How to Run the Project

### 1. Clone the Repository
```bash
    git clone https://github.com/kwanza_tukule_case_study_assessment.git
    cd kwanza_tukule_case_study_assessment
```

### 2. Set Up a Virtual Environment
```bash
    python3 -m venv venv
    source venv/bin/activate
```

### 3. Install Dependencies
```bash
    pip install -r requirements.txt
```

### 4. Run the Analysis
Execute the script to process the dataset and generate insights:
```bash
    python src/kwanza_tukule_analysis.py
```
Run the tests:
```bash
    pytest tests/ --tb=short --disable-warnings
```

### 5. View the Output
- **Console**: Logs and insights are printed with color-coded formatting for clarity.
- **Files**:
  - Strategic insights and recommendations: `strategic_insights/`
  - Bonus questions responses: `bonus_questions/`

---

## 🛠 Key Packages

- **pandas**: Data manipulation and analysis.
- **matplotlib**: Basic visualizations.
- **seaborn**: Enhanced plots.
- **plotly**: Interactive dashboard visualizations.
- **termcolor**: Color-coded console outputs.

---

### 📊 Visual Outputs

>The project generates:

- Bar charts for sales by category and business.
- Line plots for sales trends over time.
- Anomalies and insights displayed in the terminal and in file.
- Plotly rendering on localhost of the (Total Value by Category) and (Sales Over Time) via plotly

### 🌟 Highlights

- Modular and class-based implementation.
- Fully tested with pytest.
- Readable and well-documented code.
- Color-coded terminal outputs for better clarity.

### 📄 Case Study Instructions
>This project was developed following the instructions provided in the Kwanza Tukule Data Analyst Assessment. The dataset is assumed to be in the same directory and is parsed accurately.

## 📂 Project Structure

```
kwanza-tukule-analysis/
├── src/
│   ├── __init__.py
│   ├── kwanza_tukule_analysis.py  # Analysis script (Solution)
├── data/
│   └── case_study_data.xlsx       # Dataset file
├── strategic_insights_recommendation/
│   ├── customer_retention.txt
│   └── insights_overview.txt
│   ├── operational_efficiency.txt
│   └── insights_overview.txt
├── bonus_questions/
│   ├── predictive_analysis.txt
│   └── scalability_solutions.txt
├── tests/
│   ├── __init__.py
│   ├── test_kwanza_tukule_analysis.py 
├── requirements.txt               # Python dependencies
├── .gitignore                     # Files to ignore in version control
├── README.md                      # Project documentation
```

---

## ✨ Example Output

### Strategic Insights and Recommendations

Saved to `strategic_insights_recommendations/customer_rentention.txt, product_strategy.txt, operational_effeciency.txt`:
```
Product Strategy: Focus on high-value categories with consistent growth.
Customer Retention: Re-engage businesses with declining frequency using personalized offers.
Operational Efficiency: Optimize inventory for high-demand periods based on trends.
```

### Bonus Questions

Saved to `bonus_questions/predective_analysis.txt, scalability_solutions.txt`:
```
Scalability: Use distributed data storage (e.g., Hadoop, Spark) and optimize queries with indexing.
Predictive Analysis: Incorporate external factors such as economic conditions using ARIMA or ML models.
```

---

### Screenshots

![sale_trends_over_time](/screenshots/sales_trends_over_time.png)![sale_trends_over_time_plotly](/screenshots/sales_trends_over_time_plotly.png)
![total_value_by_category](/screenshots/total_value_by_category.png)![total_value_by_category_plotly](/screenshots/total_value_by_category_plotly.png)
![passing_pytests](/screenshots/tests_passing.png)![terminal_console-outputs](/screenshots/terminal_console_output.png)

## PR Request and note:

> Initiate a PR reequest to Evans Biwott on this private repo. Along with the console output as seen in the screenshot there are also output files in the strategic_insights_recommendations/ folder and the bonus_questions/ folder along with the browser rendering via plotly which address the assessment questions and also some are extra work particularly the **/strategic_insights_recommendations/insights_overview.txt** file. Thanks for taking your time to go througn my work!


## ✨ Author

Answered by [Eric Gitangu](https://developer.ericgitangu.com) for Kwanza Tukule's assessment challenge. Feedback is welcome! PR Request issued to Evans Biwott <mailto:evanson.biwott@kwanzatukule.com>
