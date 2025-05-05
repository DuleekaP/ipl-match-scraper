from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from .base_scraper import BaseScraper
from src.utils.logger import get_logger


class MatchScraper(BaseScraper):
    def __init__(self, headers=None):
        super().__init__(headers)
        self.logger = get_logger(__name__)  # Note: 'logger' with two 'g's

    def scrape_series(self, url, year):
        html = self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        matches_data = []
        
        # Find all possible match containers - more comprehensive selection
        for item in soup.find_all('div', class_=lambda x: x and 'cb-series-matches' in x):
            try:
                match_data = self._extract_match_data(item)
                if match_data:
                    match_data['Year'] = year
                    matches_data.append(match_data)
            except Exception as e:
                self.logger.error(f"Error processing match: {e}")
        
        # Additional check for matches in different container types
        alternate_containers = soup.find_all('div', class_='cb-mtch-lst')
        for container in alternate_containers:
            for item in container.find_all('div', class_='cb-col-100'):
                try:
                    match_data = self._extract_match_data(item)
                    if match_data:
                        match_data['Year'] = year
                        matches_data.append(match_data)
                except Exception as e:
                    self.logger.error(f"Error processing alternate match: {e}")
        
        return matches_data
    
    def _convert_timestamp(self, ts):
        """Convert timestamp to readable date format"""
        try:
            return datetime.fromtimestamp(int(ts)/1000).strftime('%b %d, %a')
        except:
            return "N/A"
        
    def _extract_match_data(self, item):
        """Extract match details from a single match item"""
        try:
            # Initialize with default values
            match_data = {
                'Date': "N/A",
                'Team 1': "TBC",
                'Team 2': "TBC",
                'Match Type': "N/A",
                'Venue': "N/A",
                'GMT Time': "N/A",
                'Local Time': "N/A",
                'Status': "N/A",
                'Commentary Link': None
            }

            # Get date from previous header if exists
            date_header = item.find_previous('div', class_='cb-col-100 cb-col cb-schdl-hdr')
            current_date = date_header.text.strip() if date_header else "N/A"

            match_info = item.find('div', class_='cb-col-60 cb-col cb-srs-mtchs-tm')
            if not match_info:
                return None

            # Extract teams and match type
            teams_span = match_info.find('span')
            if teams_span:
                match_text = teams_span.text.strip()
                if ' vs ' in match_text:
                    parts = match_text.split(' vs ')
                    match_data['Team 1'] = parts[0].strip()
                    team2_part = parts[1].split(',', 1)
                    match_data['Team 2'] = team2_part[0].strip()
                    match_data['Match Type'] = team2_part[1].strip() if len(team2_part) > 1 else "League Match"

            # Extract venue
            venue_div = match_info.find('div', class_='text-gray')
            if venue_div:
                match_data['Venue'] = venue_div.text.strip()

            # Extract match status
            status_tag = match_info.find('a', class_=lambda x: x and 'cb-text-' in x)
            if status_tag:
                if 'cb-text-upcoming' in status_tag['class']:
                    match_data['Status'] = "Upcoming - " + status_tag.text.strip()
                else:
                    match_data['Status'] = status_tag.text.strip()

            # Extract time information
            time_div = item.find('div', class_='cb-col-40 cb-col cb-srs-mtchs-tm')
            if time_div:
                time_spans = time_div.find_all('span')
                if time_spans:
                    match_data['GMT Time'] = time_spans[0].text.strip()
                    if len(time_spans) > 1:
                        match_data['Local Time'] = time_spans[1].text.strip()

            # Extract commentary link
            link_tag = item.find('a', class_='text-hvr-underline')
            if link_tag and 'href' in link_tag.attrs:
                match_data['Commentary Link'] = f"https://www.cricbuzz.com{link_tag['href']}"

            # Extract and format date
            timestamp_span = item.find('span', class_='schedule-date')
            if timestamp_span and 'timestamp' in timestamp_span.attrs:
                timestamp = timestamp_span['timestamp']
                match_data['Date'] = self._convert_timestamp(timestamp)
            else:
                match_data['Date'] = current_date

            return match_data

        except Exception as e:
            self.logger.error(f"Error extracting match data: {e}")
            return None