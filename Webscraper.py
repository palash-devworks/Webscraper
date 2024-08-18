import requests
from bs4 import BeautifulSoup
import os
import logging
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_robot_parser(base_url):
    rp = RobotFileParser()
    robots_url = urljoin(base_url, "/robots.txt")
    rp.set_url(robots_url)
    rp.read()
    logging.info(f"Fetched robots.txt from {robots_url}")
    
    # Log the contents of robots.txt
    logging.info("robots.txt contents:")
    for entry in rp.entries:
        logging.info(f"User-agent: {entry.useragents}")
        for rule in entry.rulelines:
            logging.info(f"{'Allow' if rule.allowance else 'Disallow'}: {rule.path}")
    
    return rp

def scrape_url():
    base_url = input("Enter the URL to scrape: ")
    logging.info(f"Starting scrape of {base_url}")
    
    rp = get_robot_parser(base_url)
    
    if not rp.can_fetch("*", base_url):
        logging.warning(f"Scraping not allowed for {base_url} according to robots.txt")
        print("Scraping is not allowed for this website according to robots.txt")
        return

    logging.info(f"Scraping allowed for {base_url}")

    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        logging.error(f"Error fetching {base_url}: {e}")
        print(f"Error fetching {base_url}: {e}")
        return

    scrape_links = soup.find_all('a')
    
    if not os.path.exists("Downloads"):
        os.makedirs("Downloads")
        logging.info("Created Downloads directory")
    
    for link in scrape_links:
        scrape_url = link.get('href')
        if scrape_url:
            full_url = urljoin(base_url, scrape_url)
            if is_valid_url(full_url):
                try:
                    scrape_response = requests.get(full_url)
                    scrape_soup = BeautifulSoup(scrape_response.content, 'html.parser')
                    
                    title = scrape_soup.find('title').text if scrape_soup.find('title') else 'Untitled'
                    content = scrape_soup.get_text()
                    
                    # Create a valid filename
                    filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
                    filename = f"Downloads/{filename[:50]}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    logging.info(f"Downloaded: {title}")
                    print(f"Downloaded: {title}")
                except requests.RequestException as e:
                    logging.error(f"Error downloading {full_url}: {e}")
                    print(f"Error downloading {full_url}: {e}")
            else:
                logging.info(f"Invalid URL: {full_url}")

    logging.info(f"Finished scraping {base_url}")

if __name__ == "__main__":
    scrape_url()