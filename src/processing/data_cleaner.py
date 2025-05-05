import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DataCleaner:
    @staticmethod
    def clean_matches_data(df):
        try:
            df['Date'] = df['Date'].replace('N/A', pd.NA)
            df['Match Type'] = df['Match Type'].str.replace(
                r'(\d+)(st|nd|rd|th) Match', r'\1\2 Match', regex=True)
            return df
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            raise