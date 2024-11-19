from flask import Flask, render_template
import pandas as pd
import requests

app = Flask(__name__)

def get_most_active_stocks():
    try:
        url = "https://finance.yahoo.com/trending-tickers"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        
        # Read tables
        from io import StringIO
        df = pd.read_html(StringIO(response.text))[0]
        
        # Clean up the Price column - extract just the first number
        df['Price'] = df['Price'].str.extract(r'(\d+\.?\d*)').astype(float)
        
        # Clean up the Change % column
        df['Change'] = df['Change %'].str.extract(r'\(([-\d.]+)%\)').astype(float)
        
        # Clean up Volume - remove any commas
        df['Volume'] = df['Volume'].str.replace(',', '').astype(str)
        
        # Select and rename columns
        result_df = df[['Symbol', 'Name', 'Price', 'Change', 'Volume']]
        result = result_df.head(10).to_dict('records')
        
        print(f"Successfully processed {len(result)} stocks")
        return result
        
    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        print("Full error details:", e)
        import traceback
        print(traceback.format_exc())
        return []

@app.route('/')
def index():
    stocks = get_most_active_stocks()
    return render_template('index.html', stocks=stocks)

if __name__ == '__main__':
    app.run(debug=True)