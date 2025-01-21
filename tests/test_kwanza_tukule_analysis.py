import pytest
import pandas as pd
import os
from src.kwanza_tukule_analysis import KwanzaTukuleAnalysis

"""
Test suite for the KwanzaTukuleAnalysis class.

This module contains test cases to validate the functionality of the KwanzaTukuleAnalysis class,
including data loading, cleaning, and analysis operations.

Test Cases:
    - test_load_data: Validates dataset loading functionality 
    - test_clean_data: Validates data cleaning operations
    - test_feature_engineering: Validates feature engineering functionality
    - test_sales_overview: Validates sales analysis functionality
    - test_trends_over_time: Validates trend analysis functionality
    - test_customer_segmentation: Validates customer segmentation
    - test_create_dashboard: Validates dashboard creation
"""

@pytest.fixture
def analysis():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    """Fixture to create analysis instance for tests"""
    return KwanzaTukuleAnalysis(file_path=os.path.join(DATA_DIR, 'case_study_data.xlsx'),
                               sheet_name='case_study_data_2025-01-16T06_4')

def test_load_data(analysis):
    """Test case to validate the dataset load functionality."""
    analysis.load_data()
    assert analysis.data is not None, "Data is not loaded!"
    assert len(analysis.data) > 0, "Dataset is empty!"
    assert isinstance(analysis.data, pd.DataFrame), "Data not loaded as DataFrame!"

def test_clean_data(analysis):
    """Test case to validate the data cleaning functionality."""
    analysis.load_data()
    analysis.clean_data()
    assert analysis.cleaned_data is not None, "Data is not cleaned!"
    assert analysis.cleaned_data.duplicated().sum() == 0, "Duplicates were not removed!"
    assert not analysis.cleaned_data.isnull().any().any(), "Missing values still present!"

def test_feature_engineering(analysis):
    """Test case to validate feature engineering."""
    analysis.load_data()
    analysis.clean_data()
    analysis.feature_engineering()
    assert 'Month-Year' in analysis.cleaned_data.columns, "Month-Year column not created!"
    assert analysis.cleaned_data['DATE'].dtype == 'datetime64[ns]', "DATE not converted to datetime!"

def test_sales_overview(analysis):
    """Test case to validate sales analysis."""
    analysis.load_data()
    analysis.clean_data()
    category_sales, business_sales = analysis.sales_overview()
    assert isinstance(category_sales, pd.DataFrame), "Category sales not returned as DataFrame!"
    assert isinstance(business_sales, pd.DataFrame), "Business sales not returned as DataFrame!"
    assert 'QUANTITY' in category_sales.columns, "QUANTITY missing from category sales!"
    assert 'UNIT PRICE' in business_sales.columns, "UNIT PRICE missing from business sales!"

def test_trends_over_time(analysis):
    """Test case to validate trend analysis."""
    analysis.load_data()
    analysis.clean_data()
    analysis.feature_engineering()
    monthly_data = analysis.trends_over_time()
    assert isinstance(monthly_data, pd.DataFrame), "Monthly data not returned as DataFrame!"
    assert 'Month-Year' in monthly_data.columns, "Month-Year column missing!"
    assert len(monthly_data) > 0, "No trends data generated!"

def test_customer_segmentation(analysis):
    """Test case to validate customer segmentation."""
    analysis.load_data()
    analysis.clean_data()
    segmentation = analysis.customer_segmentation()
    assert isinstance(segmentation, pd.DataFrame), "Segmentation not returned as DataFrame!"
    assert 'Segment' in segmentation.columns, "Segment column missing!"
    assert set(segmentation['Segment'].unique()) == {'Low Value', 'Medium Value', 'High Value'}, "Invalid segments!"


def test_create_dashboard(analysis):
    """Test case to validate dashboard creation."""
    analysis.load_data()
    analysis.clean_data()
    analysis.feature_engineering()
    analysis.monthly_data = analysis.trends_over_time()
    analysis.create_dashboard()
    # Since dashboard is interactive, we just verify the data preparation steps
    assert analysis.cleaned_data is not None, "Data not prepared for dashboard!"
    assert analysis.monthly_data is not None, "Monthly data not prepared for dashboard!"