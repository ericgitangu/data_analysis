import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

class KwanzaTukuleAnalysis:
    """
    A class to perform data analysis for the Kwanza Tukule dataset.

    Attributes:
        file_path (str): Path to the Excel file containing the dataset.
        sheet_name (str): Name of the sheet to load data from.
        data (pd.DataFrame): Raw dataset loaded from the file.
        cleaned_data (pd.DataFrame): Cleaned dataset after removing duplicates and handling missing values.
        monthly_data (pd.DataFrame): Aggregated dataset for monthly trends.
        stats_highlights (dict): Dictionary to store key statistics.
        stats_highlights (dict): Dictionary to store key statistics.
    """

    def __init__(self, file_path, sheet_name):
        """
        Initialize the class with the dataset path and sheet name.

        Args:
            file_path (str): Path to the dataset file.
            sheet_name (str): Sheet name to read data from.
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.data = None
        self.cleaned_data = None
        self.monthly_data = None
        self.stats_highlights = {}

    # Section 1: Data Cleaning and Preparation (20 points)
    def load_data(self):
        """
        Load the dataset from the specified Excel file and sheet.

        Returns:
            pd.DataFrame: The loaded dataset.
        """
        try:
            import openpyxl  # For reading Excel files
            self.data = pd.read_excel(self.file_path, sheet_name=self.sheet_name, engine='openpyxl')
            print(colored("Dataset Loaded Successfully! ✅", "green"))
            print(colored(f"Columns: {list(self.data.columns)}", "cyan"))
            print(self.data.head())
        except ImportError:
            print(colored("Error: Missing optional dependency 'openpyxl'. Please install it using `pip install openpyxl`.", "red"))
        except Exception as e:
            print(colored(f"Error loading dataset: {e}", "red"))
        return self.data

    def data_quality_assessment(self):
        """
        Inspect the dataset for missing values, duplicates, or inconsistent data types.

        Prints:
            Summary of missing values and duplicate rows.
        """
        if self.data is None:
            print(colored("Error: No data loaded. Please load the dataset first.", "red"))
            return

        print(colored("Performing Data Quality Assessment...", "blue"))
        missing_values = self.data.isnull().sum()
        duplicates = self.data.duplicated().sum()

        print(colored("Missing Values Per Column:", "yellow"))
        print(missing_values)

        print(colored(f"Number of Duplicate Rows: {duplicates}", "yellow"))
        
        if duplicates > 0:
            print(colored("Duplicates detected in the dataset.", "red"))

    def clean_data(self):
        """
        Clean the dataset by removing duplicates and handling missing values.

        Returns:
            pd.DataFrame: The cleaned dataset.
        """
        if self.data is None:
            print(colored("Error: No data loaded. Please load the dataset first.", "red"))
            return

        print(colored("Cleaning Data...", "blue"))
        self.cleaned_data = self.data.drop_duplicates().fillna(method='ffill')
        print(colored("Data cleaned successfully! ✅", "green"))
        return self.cleaned_data

    def feature_engineering(self):
        """
        Create the 'Month-Year' column for temporal analysis.

        Returns:
            pd.DataFrame: The dataset with the new 'Month-Year' column.
        """
        if self.cleaned_data is None:
            print(colored("Error: No cleaned data available. Please clean the data first.", "red"))
            return

        print(colored("Performing Feature Engineering...", "blue"))
        self.cleaned_data['DATE'] = pd.to_datetime(self.cleaned_data['DATE'], errors='coerce')
        self.cleaned_data.dropna(subset=['DATE'], inplace=True)
        self.cleaned_data['Month-Year'] = self.cleaned_data['DATE'].dt.strftime('%B %Y')
        print(colored("Feature Engineering Completed. Sample Data:", "green"))
        print(self.cleaned_data[['DATE', 'Month-Year']].head())
        return self.cleaned_data

    # Section 2: Exploratory Data Analysis (30 points)
    def sales_overview(self):
        """
        Calculate total Quantity and Value grouped by Anonymized Category and Business.

        Returns:
            tuple: DataFrames for category and business sales.
        """
        if self.cleaned_data is None:
            print(colored("Error: No cleaned data available. Please clean the data first.", "red"))
            return

        print(colored("Analyzing Sales Overview...", "blue"))
        category_sales = self.cleaned_data.groupby('ANONYMIZED CATEGORY').agg(
            {'QUANTITY': 'sum', 'UNIT PRICE': 'sum'}
        ).reset_index()

        business_sales = self.cleaned_data.groupby('ANONYMIZED BUSINESS').agg(
            {'QUANTITY': 'sum', 'UNIT PRICE': 'sum'}
        ).reset_index()

        # Visualization
        print(colored("Visualizing Sales Overview... Close to proceed with execution", "blue"))
        plt.figure(figsize=(12, 6))
        sns.barplot(data=category_sales, x='ANONYMIZED CATEGORY', y='UNIT PRICE')
        plt.title('Total Value by Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        print(colored("Sales overview completed! ✅", "green"))

        # Store key statistics
        self.stats_highlights['top_category'] = category_sales.nlargest(1, 'UNIT PRICE')['ANONYMIZED CATEGORY'].iloc[0]
        self.stats_highlights['top_category_value'] = category_sales.nlargest(1, 'UNIT PRICE')['UNIT PRICE'].iloc[0]
        self.stats_highlights['total_sales_value'] = category_sales['UNIT PRICE'].sum()
        
        return category_sales, business_sales

    def trends_over_time(self):
        """
        Analyze sales trends (Value and Quantity) by Month-Year.

        Returns:
            pd.DataFrame: Aggregated data by Month-Year.
        """
        if self.cleaned_data is None:
            print(colored("Error: No cleaned data available. Please clean the data first.", "red"))
            return

        print(colored("Analyzing Trends Over Time...", "blue"))
        self.monthly_data = self.cleaned_data.groupby('Month-Year').agg(
            {'QUANTITY': 'sum', 'UNIT PRICE': 'sum'}
        ).reset_index()

        print(colored("Visualizing Trends Over Time... Close to proceed with execution", "blue"))
        # Visualization
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.monthly_data, x='Month-Year', y='UNIT PRICE', marker='o')
        plt.title('Sales Trends Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        print(colored("Trends over time completed! ✅", "green"))

        # Store key statistics
        self.stats_highlights['peak_month'] = self.monthly_data.nlargest(1, 'UNIT PRICE')['Month-Year'].iloc[0]
        self.stats_highlights['peak_month_value'] = self.monthly_data.nlargest(1, 'UNIT PRICE')['UNIT PRICE'].iloc[0]
        self.stats_highlights['avg_monthly_value'] = self.monthly_data['UNIT PRICE'].mean()
        
        return self.monthly_data

    # Section 3: Advanced Analysis (30 points)
    def customer_segmentation(self):
        """
        Perform a segmentation analysis of businesses based on purchasing behavior.

        Returns:
            pd.DataFrame: Segmented customer groups.
        """
        if self.cleaned_data is None:
            print(colored("Error: No cleaned data available. Please clean the data first.", "red"))
            return

        print(colored("Performing Customer Segmentation...", "blue"))
        segmentation = self.cleaned_data.groupby('ANONYMIZED BUSINESS').agg(
            Total_Quantity=('QUANTITY', 'sum'),
            Total_Value=('UNIT PRICE', 'sum'),
            Frequency=('DATE', 'nunique')
        ).reset_index()

        segmentation['Segment'] = pd.qcut(segmentation['Total_Value'], q=3, labels=['Low Value', 'Medium Value', 'High Value'])
        print(colored("Customer Segmentation Completed:", "green"))
        print(segmentation.head())

        # Store key statistics
        self.stats_highlights['high_value_customers'] = len(segmentation[segmentation['Segment'] == 'High Value'])
        self.stats_highlights['avg_customer_value'] = segmentation['Total_Value'].mean()
        self.stats_highlights['top_customer'] = segmentation.nlargest(1, 'Total_Value')['ANONYMIZED BUSINESS'].iloc[0]
        self.stats_highlights['top_customer_value'] = segmentation.nlargest(1, 'Total_Value')['Total_Value'].iloc[0]
        
        return segmentation

    # Section 4: Strategic Insights and Recommendations (20 points)
    def generate_recommendations(self):
        """
        Generate strategic insights and recommendations based on analysis.

        Prints:
            Key recommendations for product strategy, customer retention, and operational efficiency.
        """
        print(colored("Generating Strategic Insights and Recommendations...", "blue"))
    
        os.makedirs('strategic_insights_recommendations', exist_ok=True)
        
        # Insights overview with comprehensive statistics
        with open('strategic_insights_recommendations/insights_overview.txt', 'w') as f:
            f.write("Strategic Insights and Recommendations\n")
            f.write("=====================================\n\n")
            f.write("Key Performance Metrics:\n")
            f.write(f"1. Sales Performance:\n")
            f.write(f"   - Total Sales Value: ${self.stats_highlights.get('total_sales_value', 0):,.2f}\n")
            f.write(f"   - Top Performing Category: {self.stats_highlights.get('top_category', 'N/A')}\n")
            f.write(f"   - Top Category Value: ${self.stats_highlights.get('top_category_value', 0):,.2f}\n\n")
            
            f.write(f"2. Temporal Analysis:\n")
            f.write(f"   - Peak Sales Month: {self.stats_highlights.get('peak_month', 'N/A')}\n")
            f.write(f"   - Peak Month Value: ${self.stats_highlights.get('peak_month_value', 0):,.2f}\n")
            f.write(f"   - Average Monthly Sales: ${self.stats_highlights.get('avg_monthly_value', 0):,.2f}\n\n")
            
            f.write(f"3. Customer Insights:\n")
            f.write(f"   - Number of High-Value Customers: {self.stats_highlights.get('high_value_customers', 0)}\n")
            f.write(f"   - Average Customer Value: ${self.stats_highlights.get('avg_customer_value', 0):,.2f}\n")
            f.write(f"   - Top Customer: {self.stats_highlights.get('top_customer', 'N/A')}\n")
            f.write(f"   - Top Customer Value: ${self.stats_highlights.get('top_customer_value', 0):,.2f}\n")
            f.write(f"   - Top Category: {self.stats_highlights.get('top_category', 'N/A')} with highest revenue potential based on historical sales data\n\n")
            f.write("=====================================\n")
        
        # Product Strategy
        top_category = self.cleaned_data.groupby('ANONYMIZED CATEGORY').agg({
            'UNIT PRICE': 'sum',
            'QUANTITY': 'sum'
        }).sort_values('UNIT PRICE', ascending=False).index[0]

        # Write initial message to file
        with open('strategic_insights_recommendations/insights_overview.txt', 'a') as f:
            f.write(f"Top Category: {top_category}\n with highest revenue potential based on historical sales data\n")
        
        # Write product strategy recommendations to file
        os.makedirs('strategic_insights_recommendations', exist_ok=True)
        with open('strategic_insights_recommendations/product_strategy.txt', 'w') as f:
            f.write("Product Strategy:\n")
            f.write(f"    - Prioritize marketing for {top_category}\n")
            f.write("    - This category shows highest revenue potential based on historical sales data\n")
            f.write("    - Focus on expanding market share in this proven high-value segment\n")

        # Print to console
        print(colored(f"Product Strategy: Prioritize marketing for {top_category}", "cyan"))
        print(colored("    - This category shows highest revenue potential based on historical sales data", "cyan"))
        print(colored("    - Focus on expanding market share in this proven high-value segment", "cyan"))

        # Customer Retention
        recent_customers = self.cleaned_data[self.cleaned_data['DATE'] >= 
            (self.cleaned_data['DATE'].max() - pd.DateOffset(months=3))]['ANONYMIZED BUSINESS'].unique()
        all_customers = self.cleaned_data['ANONYMIZED BUSINESS'].unique()
        inactive_customers = set(all_customers) - set(recent_customers)
        
        # Write customer retention recommendations to file
        with open('strategic_insights_recommendations/customer_retention.txt', 'w') as f:
            f.write("Customer Retention:\n")
            f.write(f"    - {len(inactive_customers)} businesses have reduced activity in past 3 months\n")
            f.write("    - Implement win-back campaign with targeted discounts on their most purchased items\n")
            f.write("    - Set up early warning system to flag declining purchase patterns\n")

        # Print to console
        print(colored("Customer Retention:", "cyan"))
        print(colored(f"    - {len(inactive_customers)} businesses have reduced activity in past 3 months", "cyan"))
        print(colored("    - Implement win-back campaign with targeted discounts on their most purchased items", "cyan"))
        print(colored("    - Set up early warning system to flag declining purchase patterns", "cyan"))

        # Operational Efficiency
        peak_months = self.monthly_data.nlargest(3, 'QUANTITY')['Month-Year'].tolist()
        # Write recommendations to file
        os.makedirs('strategic_insights_recommendations', exist_ok=True)
        with open('strategic_insights_recommendations/operational_efficiency.txt', 'w') as f:
            f.write("Operational Efficiency:\n")
            f.write(f"    - Increase inventory levels before peak months: {', '.join(peak_months)}\n")
            f.write("    - Implement automated reordering for top 20% selling products\n") 
            f.write("    - Consider bulk purchasing discounts during off-peak periods\n")

        # Also print to console
        print(colored("Operational Efficiency:", "cyan"))
        print(colored(f"    - Increase inventory levels before peak months: {', '.join(peak_months)}", "cyan"))
        print(colored("    - Implement automated reordering for top 20% selling products", "cyan"))
        print(colored("    - Consider bulk purchasing discounts during off-peak periods", "cyan"))

        # Write completion status to file
        with open('strategic_insights_recommendations/completion_status.txt', 'w') as f:
            f.write("Strategic Insights and Recommendations completed! ✅")
            
        # Write completion status to console
        print(colored("Strategic Insights and Recommendations completed and saved to file! ✅", "green"))

    # Section 5: Dashboard and Reporting (20 points)
    def create_dashboard(self):
        """
        Create an interactive dashboard summarizing key insights.

        The dashboard includes:
        - Total Quantity and Value by Anonymized Category.
        - Top-performing products and businesses.
        - A time-series chart of sales trends.
        - A segmentation summary of customer groups.
        """
        if self.cleaned_data is None:
            print(colored("Error: No cleaned data available. Please clean the data first.", "red"))
            return

        print(colored("Creating Interactive Dashboard...", "blue"))

        # Total Quantity and Value by Anonymized Category
        category_summary = self.cleaned_data.groupby('ANONYMIZED CATEGORY').agg(
            {'QUANTITY': 'sum', 'UNIT PRICE': 'sum'}
        ).reset_index()
        fig1 = px.bar(category_summary, x='ANONYMIZED CATEGORY', y='UNIT PRICE', title='Total Value by Category')

        # Time-Series Chart of Sales Trends
        fig2 = px.line(self.monthly_data, x='Month-Year', y='UNIT PRICE', title='Sales Trends Over Time')

        # Display Dashboard
        fig1.show()
        fig2.show()

        print(colored("Dashboard created successfully! ✅", "green"))

    # Bonus Section: Open-Ended Problem (Optional, 10 points)
    def handle_bonus_questions(self):
        """
        Address bonus questions on scalability and predictive analysis.

        Prints:
            Suggested methodologies and optimizations.
        """
        print(colored("Addressing Bonus Questions...", "blue"))
        
        # Create bonus_questions directory if it doesn't exist
        bonus_dir = os.path.join(BASE_PATH, 'bonus_questions')
        os.makedirs(bonus_dir, exist_ok=True)
        
        # Prepare content for files
        scalability_content = """Scalability Recommendations:

        1. Data Storage:
        - Implement distributed storage using Hadoop/HDFS or cloud solutions (AWS S3)
        - Partition data by date ranges for efficient querying
        - Use columnar storage formats like Parquet for better compression
        - Use Database sharding to distribute data across multiple servers
        - Ensure Database follows ACID properties - Atomicity, Consistency, Isolation, and Durability
        - Implement database replication for high availability and fault tolerance
        - Use database indexing to optimize query performance
        - Implement database backup and recovery procedures

        2. Processing Optimization:
        - Leverage Apache Spark for distributed data processing
        - Implement data streaming for real-time analysis
        - Use caching strategies for frequently accessed data
        - Using event-driven architecture to handle data streaming
        - Implement data processing pipelines for efficient data transformation and loading
        - Implement DLQs (Dead Letter Queues) to handle failed messages
        - Implement monitoring and alerting for system performance and errors
        - Implement data quality checks and validation processes
        - Implement data versioning and auditing to track changes and ensure data integrity
        - Implement data masking and anonymization to protect sensitive information
        - Use retry and exponential backoff strategies for data processing
        """

        predictive_content = """Predictive Analysis Framework:

        1. External Factors to Consider:
        - Economic indicators: GDP, inflation rates, consumer price index
        - Seasonal factors: weather patterns, holidays, events
        - Market dynamics: competitor pricing, new market entrants
        - Supply chain metrics: supplier reliability, lead times

        2. Proposed Methodology:
        - Time series models (SARIMA) incorporating seasonal components
        - Machine learning models (XGBoost, Random Forests) for multi-factor analysis
        - Neural networks for complex pattern recognition
        - Regular model retraining pipeline for accuracy maintenance
        """
        
        # Write to files
        with open(os.path.join(bonus_dir, 'scalability_solutions.txt'), 'w') as f:
            f.write(scalability_content)
            
        with open(os.path.join(bonus_dir, 'predictive_analysis.txt'), 'w') as f:
            f.write(predictive_content)

        # Print to console
        print(colored("Scalability Recommendations:", "cyan"))
        print(colored("1. Data Storage:", "cyan"))
        print(colored("   - Implement distributed storage using Hadoop/HDFS or cloud solutions (AWS S3)", "cyan"))
        print(colored("   - Partition data by date ranges for efficient querying", "cyan"))
        print(colored("   - Use columnar storage formats like Parquet for better compression", "cyan"))
        print(colored("   - Use Database sharding to distribute data across multiple servers", "cyan"))
        print(colored("   - Ensure Database follows ACID properties - Atomicity, Consistency, Isolation, and Durability", "cyan"))
        print(colored("   - Implement database replication for high availability and fault tolerance", "cyan"))
        print(colored("   - Use database indexing to optimize query performance", "cyan"))
        print(colored("   - Implement database backup and recovery procedures", "cyan"))
        print(colored("2. Processing Optimization:", "cyan"))
        print(colored("   - Leverage Apache Spark for distributed data processing", "cyan"))
        print(colored("   - Implement data streaming for real-time analysis", "cyan"))
        print(colored("   - Use caching strategies for frequently accessed data", "cyan"))
        print(colored("   - Using event-driven architecture to handle data streaming", "cyan"))
        print(colored("   - Implement data processing pipelines for efficient data transformation and loading", "cyan"))
        print(colored("   - Implement DLQs (Dead Letter Queues) to handle failed messages", "cyan"))
        print(colored("   - Implement monitoring and alerting for system performance and errors", "cyan"))
        print(colored("   - Implement data quality checks and validation processes", "cyan"))
        print(colored("   - Implement data versioning and auditing to track changes and ensure data integrity", "cyan"))
        print(colored("   - Implement data masking and anonymization to protect sensitive information", "cyan"))
        print(colored("   - Use retry and exponential backoff strategies for data processing", "cyan"))
        
        print(colored("\nPredictive Analysis Framework:", "cyan"))
        print(colored("1. External Factors to Consider:", "cyan"))
        print(colored("   - Economic indicators: GDP, inflation rates, consumer price index", "cyan"))
        print(colored("   - Seasonal factors: weather patterns, holidays, events", "cyan"))
        print(colored("   - Market dynamics: competitor pricing, new market entrants", "cyan"))
        print(colored("   - Supply chain metrics: supplier reliability, lead times", "cyan"))
        print(colored("2. Proposed Methodology:", "cyan"))
        print(colored("   - Time series models (SARIMA) incorporating seasonal components", "cyan"))
        print(colored("   - Machine learning models (XGBoost, Random Forests) for multi-factor analysis", "cyan"))
        print(colored("   - Neural networks for complex pattern recognition", "cyan"))
        print(colored("   - Regular model retraining pipeline for accuracy maintenance", "cyan"))

        print(colored("Bonus Questions addressed and saved to files! ✅", "green"))

    def run_analysis(self):
        """
        Run the entire analysis pipeline sequentially.
        """
        self.load_data()
        self.data_quality_assessment()
        self.clean_data()
        self.feature_engineering()
        self.sales_overview()
        self.trends_over_time()
        self.customer_segmentation()
        self.generate_recommendations()
        self.create_dashboard()
        self.handle_bonus_questions()

if __name__ == "__main__":
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    analysis = KwanzaTukuleAnalysis(file_path=f'{BASE_PATH}/data/case_study_data.xlsx', 
                                    sheet_name='case_study_data_2025-01-16T06_4')
    analysis.run_analysis()
