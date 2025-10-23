from flask import Flask, render_template, request

app = Flask(__name__)

# --- Simple heuristic for price estimation ---
def estimate_price(location, area, bedrooms, bathrooms, prop_type):
    base_price = 3000  # base price per sq.ft.
    if "mumbai" in location.lower():
        base_price = 12000
    elif "bangalore" in location.lower():
        base_price = 8000
    elif "delhi" in location.lower():
        base_price = 10000
    elif "pune" in location.lower():
        base_price = 7000

    # Adjust based on property type
    if "villa" in prop_type.lower():
        base_price *= 1.3
    elif "apartment" in prop_type.lower():
        base_price *= 1.0
    elif "studio" in prop_type.lower():
        base_price *= 0.9

    # Additional room factor
    base_price += (bedrooms * 300) + (bathrooms * 150)

    # Estimated total price
    min_price = base_price * area * 0.9
    max_price = base_price * area * 1.1
    return f"₹{min_price:,.0f} - ₹{max_price:,.0f}"

# --- Generate marketing-style description ---
def generate_listing(location, area, bedrooms, bathrooms, prop_type, amenities):
    desc = f"""
    Experience modern living with this stunning {bedrooms}-bedroom, {bathrooms}-bathroom {prop_type} in {location}.
    Spanning {area} sq.ft., this property offers a perfect blend of comfort and elegance.
    Enjoy premium amenities including {amenities}.
    Ideal for families or professionals looking for convenience and style.
    Don't miss this rare opportunity — book your visit today!
    """
    return desc.strip()

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        location = request.form.get("location")
        area = float(request.form.get("area", 0))
        bedrooms = int(request.form.get("bedrooms", 0))
        bathrooms = int(request.form.get("bathrooms", 0))
        prop_type = request.form.get("type")
        amenities = request.form.get("amenities")

        estimated_price = estimate_price(location, area, bedrooms, bathrooms, prop_type)
        listing_text = generate_listing(location, area, bedrooms, bathrooms, prop_type, amenities)

        result = {
            "price": estimated_price,
            "listing": listing_text
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
