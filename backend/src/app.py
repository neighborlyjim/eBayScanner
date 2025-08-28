# app.py - Main Flask application using DRY principles
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import config
import scout
from models import db, TrackedItem, BuyItNowAverage
from ebay_api import ebay_api
import logging
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
alerts = []

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = config.config.database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize database with app
db.init_app(app)

def poll_ebay():
    global alerts
    new = []
    for item in scout.search_ending_soon():
        if scout.is_undervalued(item):
            new.append({
                "title": item.title,
                "price": item.price.value,
                "url": item.item_web_url
            })
    alerts = new  # simple overwrite; you can append/dedupe instead

scheduler = BackgroundScheduler()
scheduler.add_job(poll_ebay, "interval", minutes=5)
scheduler.start()

@app.route('/api/search', methods=['POST'])
def api_search():
    """New API endpoint for frontend to search eBay deals"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_price = data.get('maxPrice', 1000)
        max_time_hours = data.get('maxTimeHours', 24)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
            
        logging.debug(f"API Search: {query}, maxPrice: {max_price}, maxTime: {max_time_hours}h")
        
        # Search for undervalued deals using your eBay API
        deals = scout.search_undervalued_deals(query, max_price, max_time_hours)
        
        return jsonify({
            'results': deals,
            'query': query,
            'filters': {
                'maxPrice': max_price,
                'maxTimeHours': max_time_hours
            }
        })
        
    except Exception as e:
        logging.error(f"API search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle both form data and JSON
        query = request.form.get('query') or request.json.get('query') if request.is_json else request.form.get('query')
        logging.debug(f"Search query received: {query}")

        if query:
            try:
                # Use centralized eBay API helper
                response = ebay_api.find_items_by_keywords(query)
                items = ebay_api.extract_items_from_response(response)
                logging.debug(f"eBay API response: {items}")

                # Return JSON for frontend API calls
                if request.is_json:
                    results = []
                    for item in items:
                        results.append({
                            'title': item.title,
                            'price': f"${item.sellingStatus.currentPrice.value}",
                            'url': item.viewItemURL
                        })
                    return {'results': results}
                
                # Render the results on the index page for form submissions
                return render_template('index.html', results=items)
            except Exception as e:
                logging.error(f"Error fetching eBay data: {e}")
                if request.is_json:
                    return {'error': 'Error fetching data from eBay.'}, 500
                return render_template('index.html', results=[], error="Error fetching data from eBay.")

    return render_template('index.html', results=[])

@app.route('/listings', methods=['GET'])
def listings():
    # Fetch all tracked items from the database
    tracked_items = TrackedItem.query.all()
    return render_template('listings.html', tracked_items=tracked_items)

@app.route('/add_to_tracking', methods=['POST'])
def add_to_tracking():
    item_id = request.form.get('item_id')
    logging.debug(f"Item ID to track: {item_id}")

    try:
        # Use centralized eBay API helper
        response = ebay_api.find_item_by_id(item_id)
        items = ebay_api.extract_items_from_response(response)
        
        if not items:
            logging.error("No item found with the given ID")
            return redirect('/', error="Item not found.")
            
        item = items[0]

        # Extract relevant details
        title = item.title
        price = item.sellingStatus.currentPrice.value
        url = item.viewItemURL
        upc = item.productId.value if hasattr(item, 'productId') else None

        # Add to database
        tracked_item = TrackedItem(
            id=item_id,
            title=title, 
            current_price=float(price), 
            end_time=item.listingInfo.endTime,
            upc=upc
        )
        db.session.add(tracked_item)
        db.session.commit()

        logging.debug(f"Item added to tracking: {title}")
        return redirect('/listings')
    except Exception as e:
        logging.error(f"Error adding item to tracking: {e}")
        return redirect('/', error="Failed to add item to tracking.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
