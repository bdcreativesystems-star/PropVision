from bs4 import BeautifulSoup
import os
from database import init_db, insert_listing

def scrape_listings():
    """Scrape listings from the sample HTML file."""
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "sample_listings.html")

    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    listings = []

    for listing in soup.find_all("div", class_="listing"):
        # Extract and clean data
        price_text = listing.find("span", class_="price").text.strip().replace("$", "").replace(",", "")
        address = listing.find("span", class_="address").text.strip()
        sqft_text = listing.find("span", class_="sqft").text.strip().replace(",", "")

        # Convert price and sqft to integers safely
        try:
            price = int(price_text)
        except ValueError:
            price = 0

        try:
            sqft = int(sqft_text)
        except ValueError:
            sqft = 0

        listings.append({
            "price": price,
            "address": address,
            "sqft": sqft
        })

    return listings


def save_listings_to_db(listings):
    """Save scraped listings into the database."""
    for item in listings:
        insert_listing(item["address"], item["price"], item["sqft"])


if __name__ == "__main__":
    # Initialize DB
    init_db()

    # Scrape and save
    listings = scrape_listings()
    save_listings_to_db(listings)

    print("Listings scraped and saved to database!")
    for item in listings:
        print(item)
