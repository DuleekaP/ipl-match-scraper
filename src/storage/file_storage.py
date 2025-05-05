import pandas as pd
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FileStorage:
    def __init__(self, output_dir='data/outputs'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_to_csv(self, df, filename):
        path = self.output_dir / f"{filename}.csv"
        df.to_csv(path, index=False)
        logger.info(f"Saved data to {path}")