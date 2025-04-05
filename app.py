from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_csv("realestate_data.csv")

    # Clean and convert
    df['Price'] = df['Price'].astype(str).str.replace(r'[$,]', '', regex=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
    df['Suburb'] = df['Suburb'].fillna('').astype(str)
    df['Beds'] = pd.to_numeric(df['Beds'], errors='coerce').fillna(0).astype(int)

    # Filters
    suburb = request.args.get('suburb', '').strip().lower()
    min_price = request.args.get('min_price', type=float)
    min_beds = request.args.get('min_beds', type=int)

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

@app.route('/export', methods=['POST'])
def export():
    df = pd.read_csv("realestate_data.csv")
    # Apply filters like in index
    df['Price'] = df['Price'].astype(str).str.replace(r'[$,]', '', regex=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
    df['Suburb'] = df['Suburb'].fillna('').astype(str)
    df['Beds'] = pd.to_numeric(df['Beds'], errors='coerce').fillna(0).astype(int)

    suburb = request.args.get('suburb', '').strip().lower()
    min_price = request.args.get('min_price', type=float)
    min_beds = request.args.get('min_beds', type=int)

    if suburb:
        df = df[df['Suburb'].str.lower().str.contains(suburb)]
    if min_price is not None:
        df = df[df['Price'] >= min_price]
    if min_beds is not None:
        df = df[df['Beds'] >= min_beds]

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(io.BytesIO(buffer.read().encode()), mimetype='text/csv', as_attachment=True, download_name='filtered_listings.csv')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)

