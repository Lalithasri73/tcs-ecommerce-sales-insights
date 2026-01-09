from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Logging (TCS Standard)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load data
DATA_PATH = 'C:/Users/HP/Desktop/ecommerce-sales-insights/data/processed/sales_clean.csv'
df = pd.read_csv(DATA_PATH) if os.path.exists(DATA_PATH) else pd.DataFrame()
logger.info(f"Loaded {len(df)} rows")

@app.route('/api/v1/health')
def health():
    return jsonify({
        'status': 'healthy',
        'rows': len(df),
        'date_range': f"{df['order_date'].min()} to {df['order_date'].max()}" if not df.empty else 'no_data'
    })

@app.route('/api/v1/kpis')
def kpis():
    if df.empty:
        return jsonify({'error': 'No data loaded'}), 503
    
    return jsonify({
        'total_sales': round(df['total_price'].sum(), 2),
        'orders': int(df['order'].nunique()),
        'aov': round(df.groupby('order')['total_price'].sum().mean(), 2),
        'customers': int(df['customer_id'].nunique()),
        'top_category': df['product_category'].mode().iloc[0]
    })

@app.route('/api/v1/categories')
def categories():
    return jsonify(df['product_category'].value_counts().head(10).to_dict())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


