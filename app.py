from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_csv("realestate_data.csv")

    # Clean and convert data
    df['Price'] = df['Price'].astype(str).str.replace(r'[$,]', '', regex=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
    df['Suburb'] = df['Suburb'].fillna('').astype(str)
    df['Beds'] = pd.to_numeric(df['Beds'], errors='coerce').fillna(0).astype(int)

    # Get filter values from request
    suburb = request.args.get('suburb', '').strip().lower()
    min_price = request.args.get('min_price', type=float)
    min_beds = request.args.get('min_beds', type=int)

    # Apply filters
    if suburb:
        df = df[df['Suburb'].str.lower().str.contains(suburb)]
    if min_price is not None:
        df = df[df['Price'] >= min_price]
    if min_beds is not None:
        df = df[df['Beds'] >= min_beds]

    # Chart data
    avg_prices = df.groupby('Suburb')['Price'].mean().sort_values(ascending=False)
    chart_labels = avg_prices.index.tolist()
    chart_data = [round(p, 0) for p in avg_prices.values]

    listings = df.to_dict(orient="records")
    return render_template(
        "index.html",
        listings=listings,
        chart_labels=chart_labels,
        chart_data=chart_data
    )

if __name__ == "__main__":
    app.run(debug=True)
