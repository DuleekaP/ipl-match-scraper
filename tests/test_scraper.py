import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def convert_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts)/1000).strftime('%b %d, %a')
    except:
        return "N/A"

def scrape_series_match_data(url, headers, year):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    matches_data = []
    current_date = None

    for item in soup.find_all('div', class_=['cb-col-100 cb-col cb-series-matches', 
                                          'cb-col-100 cb-col cb-series-brdr cb-series-matches']):
        # Date header check
        date_header = item.find_previous('div', class_='cb-col-100 cb-col cb-schdl-hdr')
        if date_header:
            current_date = date_header.text.strip()
        
        # Match info extraction
        match_info = item.find('div', class_='cb-col-60 cb-col cb-srs-mtchs-tm')
        if not match_info:
            continue

        try:
            # Teams extraction
            teams_span = match_info.find('span')
            if teams_span:
                match_text = teams_span.text.strip()
                if ' vs ' in match_text:
                    parts = match_text.split(' vs ')
                    team1 = parts[0].strip()
                    team2, *match_type = parts[1].split(',', 1)
                    team2 = team2.strip()
                    match_type = match_type[0].strip() if match_type else "League Match"
                else:
                    team1 = team2 = "TBC"
                    match_type = match_text
            else:
                team1 = team2 = "TBC"
                match_type = "N/A"
            
            # Venue
            venue = match_info.find('div', class_='text-gray').text.strip() if match_info.find('div', class_='text-gray') else "N/A"
            
            # Status
            status_tag = match_info.find('a', class_=lambda x: x and 'cb-text-' in x)
            if status_tag:
                status = "Upcoming - " + status_tag.text.strip() if 'cb-text-upcoming' in status_tag['class'] else status_tag.text.strip()
            else:
                status = "N/A"
            
            # Time
            time_div = item.find('div', class_='cb-col-40 cb-col cb-srs-mtchs-tm')
            if time_div:
                time_spans = time_div.find_all('span')
                gmt_time = time_spans[0].text.strip() if time_spans else "N/A"
                local_time = time_spans[1].text.strip() if len(time_spans) > 1 else "N/A"
            else:
                gmt_time = local_time = "N/A"

            # Commentary link
            commentary_link = None
            link_tag = item.find('a', class_='text-hvr-underline')
            if link_tag and 'href' in link_tag.attrs:
                commentary_link = "https://www.cricbuzz.com" + link_tag['href']

            # Timestamp
            timestamp_span = item.find('span', class_='schedule-date')
            timestamp = timestamp_span['timestamp'] if timestamp_span and 'timestamp' in timestamp_span.attrs else "N/A"
            formatted_date = convert_timestamp(timestamp) if timestamp != "N/A" else current_date

            matches_data.append({
                'Date': formatted_date,
                'Team 1': team1,
                'Team 2': team2,
                'Match Type': match_type,
                'Venue': venue,
                'GMT Time': gmt_time,
                'Local Time': local_time,
                'Status': status,
                'Commentary Link': commentary_link,
                'Year': year
            })

        except Exception as e:
            print(f"Error processing match: {e}")
            continue

    if matches_data:
        df = pd.DataFrame(matches_data)
        df['Date'] = df['Date'].replace('N/A', pd.NA)
        df['Match Type'] = df['Match Type'].str.replace(r'(\d+)(st|nd|rd|th) Match', r'\1\2 Match', regex=True)
        filename = f'ipl_{year}_matches.csv'
        df.to_csv(filename, index=False)
        print(f"Successfully saved {len(df)} matches to {filename}")

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for year in range(2008, 2026):
        archive_url = f"https://www.cricbuzz.com/cricket-scorecard-archives/{year}"
        try:
            response = requests.get(archive_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.find_all('div', class_='cb-srs-lst-itm'):
                link_tag = item.find('a', class_='text-hvr-underline', 
                                    title=lambda t: t and 'Indian Premier League' in t)
                if link_tag:
                    full_series_url = f"https://www.cricbuzz.com{link_tag['href']}"
                    print(f"Found IPL {year} series: {full_series_url}")
                    scrape_series_match_data(full_series_url, headers, year)
                    break  # Process only the first found series per year

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch archive for {year}: {e}")
            continue

if __name__ == '__main__':
    main()