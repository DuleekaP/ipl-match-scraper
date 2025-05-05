from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SeriesScraper(BaseScraper):
    def find_series_links(self, year):
        archive_url = f"https://www.cricbuzz.com/cricket-scorecard-archives/{year}"
        html = self.fetch_page(archive_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        for item in soup.find_all('div', class_='cb-srs-lst-itm'):
            link_tag = item.find('a', class_='text-hvr-underline', 
                              title=lambda t: t and 'Indian Premier League' in t)
            if link_tag:
                yield f"https://www.cricbuzz.com{link_tag['href']}"