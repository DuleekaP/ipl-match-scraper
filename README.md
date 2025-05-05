# IPL Match Scraper

A Python pipeline to scrape, process, and store Indian Premier League (IPL) match data from Cricbuzz.

## Features

- Scrapes match data from 2008 to present
- Cleans and transforms raw data
- Stores in multiple formats (CSV, JSON, database)
- Generates visualizations
- Comprehensive error handling

## Installation

1. Clone the repository:
   git clone https://github.com/DuleekaP/ipl-match-scraper.git
   cd ipl-match-scraper

2. Create and activate virtual environment:
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate    # Windows

3. Install dependencies:
    pip install -r requirements.txt


## Usage

Run the complete pipeline:
    python run.py

For specific years and output format
    python run.py --start-year 2015 --end-year 2020 --output json

To generate visualizations (in progress)
    python run.py --visualize

## Project Structure

    ipl-match-scraper/
    ├── config/           # Configuration files
    ├── data/             # Data storage
    ├── src/              # Source code
    ├── tests/            # Unit tests
    ├── run.py            # Main pipeline
    ├── requirements.txt  # Dependencies
    └── README.md         # Documentation