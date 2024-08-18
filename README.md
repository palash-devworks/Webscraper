# General Web Scraper

A Python-based web scraper that downloads content from a given URL and its linked pages while respecting robots.txt rules.

## Features

- Scrapes a user-specified URL
- Downloads content from all linked pages
- Respects robots.txt rules
- Saves content as text files
- Handles both relative and absolute URLs
- Validates URLs before scraping
- Basic error handling

## Requirements

- Python 3.x
- requests
- beautifulsoup4

## Installation

1. Clone this repository or download the `Webscraper.py` file.
2. Install required packages:
   ```
   pip install requests beautifulsoup4
   ```

## Usage

1. Run the script:
   ```
   python Webscraper.py
   ```
2. Enter the URL you want to scrape when prompted.
3. The script will create a "Downloads" folder and save the scraped content as text files, respecting robots.txt rules.

## Limitations

- Does not handle JavaScript-rendered content
- Basic error handling
- Only checks robots.txt for the wildcard user-agent ("*")

## Ethical Considerations

This scraper respects robots.txt rules, but users should still be aware of and comply with website terms of service and ethical scraping practices.

## License

[MIT License](https://opensource.org/licenses/MIT)