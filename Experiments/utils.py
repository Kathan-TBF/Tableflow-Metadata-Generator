# utils.py

import pandas as pd
from constants import METADATA_SHEETS, SHEET_SCHEMAS

class MetadataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.summary = {}

    def load_excel(self):
        try:
            xls = pd.ExcelFile(self.file_path)
            for sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet)
                self.data[sheet] = df
            return True
        except Exception as e:
            return f"❌ Error loading Excel: {e}"

    def summarize(self):
        if not self.data:
            return "❌ No data loaded to summarize."
        
        for sheet, df in self.data.items():
            summary_info = {
                'rows': df.shape[0],
                'columns': df.shape[1],
                'columns_list': df.columns.tolist(),
                'null_columns': df.isnull().sum()[df.isnull().sum() > 0].to_dict()
            }
            self.summary[sheet] = summary_info
        return self.summary
    
class RawDataLoader:
    """Handles user-uploaded raw business data"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.tables = {}

    def load_user_excel(self):
        try:
            xls = pd.ExcelFile(self.file_path)
            for sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet)
                self.tables[sheet] = df
            return True
        except Exception as e:
            return f"❌ Error loading User Raw Excel: {e}"

    def summarize_user_data(self):
        """Only summarize actual tables (no system sheets)"""
        summary = {}
        for sheet, df in self.tables.items():
            summary[sheet] = df.columns.tolist()
        return summary

def export_single_metadata(df, output_path):
    """ (OLD) If you only export a single sheet like Modules, use this """
    expected_cols = ['Module', 'Parent Module', 'Type', 'Color', 'Icon']
    df = df[expected_cols]  # Ensure schema integrity
    df.to_excel(output_path, index=False)

def export_full_metadata(all_sheets_dict, output_file):
    with pd.ExcelWriter(output_file) as writer:
        for sheet_name in METADATA_SHEETS:
            df = all_sheets_dict.get(sheet_name, pd.DataFrame())
            df = validate_sheet_columns(sheet_name, df)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def validate_sheet_columns(sheet_name, df):
    """ Ensure the dataframe strictly follows schema defined in constants.py """
    expected_cols = SHEET_SCHEMAS[sheet_name]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""  # Fill missing columns with empty strings
    return df[expected_cols]  # Ensure correct column ordering