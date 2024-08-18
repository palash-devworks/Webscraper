import requests
from bs4 import BeautifulSoup
import os
import logging
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from collections import defaultdict
import time

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_robot_parser(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    rp = RobotFileParser()
    robots_url = urljoin(base_url, "/robots.txt")
    
    logging.info(f"Fetching robots.txt from {robots_url}")
    try:
        rp.set_url(robots_url)
        rp.read()
        logging.info(f"Successfully fetched robots.txt from {robots_url}")
    except Exception as e:
        logging.error(f"Error fetching robots.txt from {robots_url}: {e}")
        return None
    
    # Log the contents of robots.txt
    logging.info(f"robots.txt contents for {base_url}:")
    for entry in rp.entries:
        logging.info(f"User-agent: {entry.useragents}")
        for rule in entry.rulelines:
            logging.info(f"{'Allow' if rule.allowance else 'Disallow'}: {rule.path}")
    
    return rp

def scrape_url():
    base_url = input("Enter the URL to scrape: ")
    logging.info(f"Starting scrape of {base_url}")
    
    robot_parsers = defaultdict(lambda: None)
    
    def can_fetch(url):
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        if robot_parsers[domain] is None:
            robot_parsers[domain] = get_robot_parser(url)
        if robot_parsers[domain] is None:
            logging.warning(f"Unable to fetch robots.txt for {domain}. Assuming scraping is allowed.")
            return True
        allowed = robot_parsers[domain].can_fetch("*", url)
        logging.info(f"Robots.txt {'allows' if allowed else 'disallows'} scraping of {url}")
        return allowed
    
    if not can_fetch(base_url):
        logging.warning(f"Scraping not allowed for {base_url} according to robots.txt")
        print("Scraping is not allowed for this website according to robots.txt")
        return

    logging.info(f"Scraping allowed for {base_url}")

    try:
        logging.info(f"Fetching content from {base_url}")
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        logging.info(f"Successfully fetched content from {base_url}")
    except requests.RequestException as e:
        logging.error(f"Error fetching {base_url}: {e}")
        print(f"Error fetching {base_url}: {e}")
        return

    scrape_links = soup.find_all('a')
    logging.info(f"Found {len(scrape_links)} links on {base_url}")
    
    if not os.path.exists("Downloads"):
        os.makedirs("Downloads")
        logging.info("Created Downloads directory")
    
    for link in scrape_links:
        scrape_url = link.get('href')
        if scrape_url:
            full_url = urljoin(base_url, scrape_url)
            logging.info(f"Processing URL: {full_url}")
            if is_valid_url(full_url):
                logging.info(f"Valid URL: {full_url}")
                if can_fetch(full_url):
                    try:
                        logging.info(f"Fetching content from {full_url}")
                        scrape_response = requests.get(full_url)
                        scrape_soup = BeautifulSoup(scrape_response.content, 'html.parser')
                        
                        title = scrape_soup.find('title').text if scrape_soup.find('title') else 'Untitled'
                        content = scrape_soup.get_text()
                        
                        # Create a valid filename
                        filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
                        filename = f"Downloads/{filename[:50]}.txt"
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        logging.info(f"Downloaded: {title} - Saved as {filename}")
                        print(f"Downloaded: {title}")
                        
                        # Respect crawl-delay if specified
                        if robot_parsers[urlparse(full_url).netloc]:
                            delay = robot_parsers[urlparse(full_url).netloc].crawl_delay("*")
                            if delay:
                                logging.info(f"Respecting crawl-delay of {delay} seconds")
                                time.sleep(delay)
                    except requests.RequestException as e:
                        logging.error(f"Error downloading {full_url}: {e}")
                        print(f"Error downloading {full_url}: {e}")
                else:
                    logging.info(f"Skipping {full_url}: Not allowed by robots.txt")
                    print(f"Skipping {full_url}: Not allowed by robots.txt")
            else:
                logging.warning(f"Invalid URL: {full_url}")

    logging.info(f"Finished scraping {base_url}")

if __name__ == "__main__":
    scrape_url()