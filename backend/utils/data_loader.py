from flask import Flask, jsonify
from flask_cors import CORS
from utils.data_loader import load_sales_data  # ← NEW
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# TCS Production Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Load data with utils (TCS Standard)
df = load_sales_data()  # ← UPDATED

@app.route('/api/v1/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'rows': len(df),
        'columns': list(df.columns) if not df.empty else [],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v1/kpis')
def kpis():
    if df.empty:
        return jsonify({'error': 'No data loaded'}), 503
    
    try:
        return jsonify({
            'total_sales': round(float(df['total_price'].sum()), 2),
            'orders': int(df['order'].nunique()),
            'aov': round(float(df.groupby('order')['total_price'].sum().mean()), 2),
            'customers': int(df['customer_id'].nunique()),
            'top_category': df['product_category'].mode().iloc[0] if not df['product_category'].empty else 'N/A'
        })
    except Exception as e:
        logger.error(f"KPIs error: {e}")
        return jsonify({'error': 'Calculation failed'}), 500

@app.route('/api/v1/categories')
def categories():
    if df.empty:
        return jsonify({})
    return jsonify(df['product_category'].value_counts().head(10).to_dict())

@app.route('/api/v1/trends')
def trends():
    if df.empty:
        return jsonify([])
    monthly = df.set_index('order_date')['total_price'].resample('M').sum()
    return jsonify([{
        'month': idx.strftime('%Y-%m'),
        'sales': round(float(val), 0)
    } for idx, val in monthly.items() if val > 0])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
