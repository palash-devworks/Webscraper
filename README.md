# General Web Scraper

A Python-based web scraper that downloads content from a given URL and its linked pages while respecting individual robots.txt rules and providing comprehensive logging of its activities.

## Features

- Scrapes a user-specified URL and its linked pages
- Respects robots.txt rules for each individual domain
- Provides comprehensive logging of all activities, including:
  - robots.txt parsing and interpretation
  - URL validation
  - Content fetching and saving
  - Error handling
- Saves content as text files
- Handles both relative and absolute URLs
- Validates URLs before scraping
- Respects crawl-delay if specified in robots.txt
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
3. The script will check the robots.txt file for each domain it encounters and proceed if scraping is allowed.
4. It will create a "Downloads" folder and save the scraped content as text files.
5. Check the `scraper.log` file for comprehensive information about the scraping process, including:
   - robots.txt parsing results for each domain
   - URL validation results
   - Content fetching and saving details
   - Any errors encountered during the process

## Example

Here's an example of how to use the web scraper to scrape Paul Graham's articles page:

```
$ python Webscraper.py
Enter the URL to scrape: https://www.paulgraham.com/articles.html
```

After running the script, you'll find the scraped content in the "Downloads" folder. Each article will be saved as a separate text file, with the filename based on the article's title. For example:

- `Downloads/How_to_Do_Great_Work.txt`
- `Downloads/The_Lesson_to_Unlearn.txt`
- `Downloads/How_to_Be_an_Expert_in_a_Changing_World.txt`

The `scraper.log` file will contain detailed information about the scraping process, including:

- Confirmation that robots.txt allows scraping
- The total number of links found on the articles page
- Each article URL processed
- Successful downloads and any errors encountered

Note: This example assumes that scraping is allowed by www.paulgraham.com's robots.txt. Always check the website's terms of service and robots.txt before scraping, and use the data responsibly and ethically.

## Limitations

- Does not handle JavaScript-rendered content
- Only checks robots.txt for the wildcard user-agent ("*")
- Basic error handling

## Ethical Considerations

This scraper respects robots.txt rules for each individual domain it encounters, including crawl-delay directives, and provides comprehensive logging of its activities. However, users should still be aware of and comply with website terms of service and ethical scraping practices.

## License

[MIT License](https://opensource.org/licenses/MIT)