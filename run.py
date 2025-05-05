from src.scraper.series_scraper import SeriesScraper
from src.scraper.match_scraper import MatchScraper
from src.processing.data_cleaner import DataCleaner
from src.storage.file_storage import FileStorage
from src.utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

def main():
    years = range(2008, 2026)
    series_scraper = SeriesScraper()
    match_scraper = MatchScraper()
    cleaner = DataCleaner()
    storage = FileStorage()

    for year in years:
        try:
            logger.info(f"Processing year {year}")
            for series_url in series_scraper.find_series_links(year):
                matches = match_scraper.scrape_series(series_url, year)
                if matches:
                    df = cleaner.clean_matches_data(pd.DataFrame(matches))
                    storage.save_to_csv(df, f"ipl_{year}_matches")
        except Exception as e:
            logger.error(f"Failed to process year {year}: {e}")

if __name__ == '__main__':
    main()