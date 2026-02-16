from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB_FILE = "listings.db"


def get_listings(min_price=0, max_price=float('inf'), min_sqft=0, max_sqft=float('inf')):
    """Retrieve listings from DB with optional filters."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT address, price, sqft FROM listings")
    rows = cursor.fetchall()
    conn.close()

    listings = []
    for r in rows:
        address, price, sqft = r
        if min_price <= price <= max_price and min_sqft <= sqft <= max_sqft:
            price_per_sqft = round(price / sqft, 2) if sqft > 0 else 0
            listings.append({
                "address": address,
                "price": price,
                "sqft": sqft,
                "price_per_sqft": price_per_sqft
            })
    return listings


def get_analytics(listings):
    total_price = sum(l["price"] for l in listings)
    total_sqft = sum(l["sqft"] for l in listings if l["sqft"] > 0)
    num_listings = len(listings)

    avg_price = round(total_price / num_listings, 2) if num_listings > 0 else 0
    avg_price_per_sqft = round(total_price / total_sqft, 2) if total_sqft > 0 else 0

    return {
        "num_listings": num_listings,
        "avg_price": avg_price,
        "avg_price_per_sqft": avg_price_per_sqft
    }


@app.route("/", methods=["GET"])
def dashboard():
    # Get filter values from URL parameters
    min_price = int(request.args.get("min_price", 0))
    max_price = int(request.args.get("max_price", 10000000))
    min_sqft = int(request.args.get("min_sqft", 0))
    max_sqft = int(request.args.get("max_sqft", 10000000))

    listings = get_listings(min_price, max_price, min_sqft, max_sqft)
    analytics = get_analytics(listings)

    # Prepare chart data
    chart_labels = [l["address"] for l in listings]
    chart_prices = [l["price"] for l in listings]
    chart_ppsqft = [l["price_per_sqft"] for l in listings]

    return render_template(
        "dashboard.html",
        listings=listings,
        analytics=analytics,
        chart_labels=chart_labels,
        chart_prices=chart_prices,
        chart_ppsqft=chart_ppsqft,
        min_price=min_price,
        max_price=max_price,
        min_sqft=min_sqft,
        max_sqft=max_sqft
    )


if __name__ == "__main__":
    app.run(debug=True)
