from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_domain(suburb="bondi-beach-nsw-2026", pages=1):
    listings = []

    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for page in range(1, pages + 1):
        url = f"https://www.domain.com.au/sale/{suburb}/?page={page}"
        print(f"Scraping: {url}")
        driver.get(url)
        time.sleep(3)

        cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='listing-card']")

        for card in cards:
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "[data-testid='listing-card-link']")
                price_el = card.find_element(By.CSS_SELECTOR, "[data-testid='listing-card-price']")
                features = card.find_elements(By.CSS_SELECTOR, "[data-testid='property-features'] span")

                beds = features[0].text if len(features) > 0 else "N/A"
                baths = features[1].text if len(features) > 1 else "N/A"
                cars = features[2].text if len(features) > 2 else "N/A"

                listings.append({
                    "Title": title_el.text.strip(),
                    "Price": price_el.text.strip(),
                    "Beds": beds,
                    "Baths": baths,
                    "Cars": cars,
                    "URL": title_el.get_attribute("href")
                })

            except Exception as e:
                print("Error parsing listing:", e)

    driver.quit()
    return pd.DataFrame(listings)

if __name__ == "__main__":
    df = scrape_domain(pages=2)
    print(df.head())
    df.to_csv("realestate_data.csv", index=False)
    print("✅ Saved to realestate_data.csv")
