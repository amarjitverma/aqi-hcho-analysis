"""
Export Utilities - Export data in various formats
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

def export_to_csv(data, filename=None):
    """Export data to CSV format"""
    if filename is None:
        filename = f"aqi-data-{datetime.now().strftime('%Y%m%d')}.csv"
    
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    
    return st.download_button(
        label="📥 Download as CSV",
        data=csv_buffer.getvalue(),
        file_name=filename,
        mime="text/csv",
        key=f"csv_{filename}"
    )

def export_to_json(data, filename=None):
    """Export data to JSON format"""
    if filename is None:
        filename = f"aqi-data-{datetime.now().strftime('%Y%m%d')}.json"
    
    json_str = data.to_json(orient='records')
    
    return st.download_button(
        label="📥 Download as JSON",
        data=json_str,
        file_name=filename,
        mime="application/json",
        key=f"json_{filename}"
    )

def export_to_excel(data, filename=None):
    """Export data to Excel format"""
    if filename is None:
        filename = f"aqi-data-{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name='Data', index=False)
    
    return st.download_button(
        label="📥 Download as Excel",
        data=excel_buffer.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"excel_{filename}"
    )

def generate_report_filename(report_type):
    """Generate report filename with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{report_type}_{timestamp}"
