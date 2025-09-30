import requests
from bs4 import BeautifulSoup
import time  # For good practice: always add a small delay

# --- Configuration ---
# ⚠ Disclaimer: Always check a website's robots.txt and Terms of Service
# before scraping. Use this practice site for safety and legality.
TARGET_URL = 'http://quotes.toscrape.com/'
OUTPUT_FILENAME = 'headlines.txt'


# ---------------------

def scrape_news_headlines(url):
    """
    Fetches HTML from a URL and extracts the main text elements.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        list: A list of extracted headline/text strings.
    """
    print(f"🚀 Attempting to fetch URL: {url}")
    try:
        # 1. Use requests to fetch HTML
        # Add a simple User-Agent header to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # 2. Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- CRITICAL STEP: HTML TAG IDENTIFICATION ---
        # The hint suggests using <h2> or <title> tags.
        # For a real news site, you'd inspect the source to find the class
        # of the element holding the headline (e.g., soup.find_all('h2', class_='headline-text')).
        # For the demo site, the main text (quotes) is in a <span> with class 'text'.

        headlines = []
        # Find all <span> tags with the class 'text'
        text_elements = soup.find_all('span', class_='text')

        for element in text_elements:
            # .get_text(strip=True) extracts the text and removes leading/trailing whitespace
            headlines.append(element.get_text(strip=True))

        print(f"✅ Successfully found {len(headlines)} items.")
        return headlines

    except requests.exceptions.RequestException as e:
        print(f"❌ Error during request to {url}: {e}")
        return []
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return []


def save_to_txt(data, filename):
    """
    3. Save the titles in a .txt file.

    Args:
        data (list): List of strings to write.
        filename (str): Name of the output file.
    """
    if not data:
        print("🛑 No data to save.")
        return

    try:
        # 'w' mode opens the file for writing (and creates/overwrites it)
        with open(filename, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(item + '\n')  # Write each item on a new line
        print(f"💾 Data successfully saved to {filename}")
    except IOError as e:
        print(f"❌ Error saving file {filename}: {e}")


def main():
    """Main function to run the scraping task."""
    # Introduce a small delay before scraping
    time.sleep(1)

    # Scrape the data
    scraped_data = scrape_news_headlines(TARGET_URL)

    # Save the data
    save_to_txt(scraped_data, OUTPUT_FILENAME)


if __name__ == "__main__":
    main()