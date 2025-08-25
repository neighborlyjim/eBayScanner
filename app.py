# app.py
from flask import Flask, render_template_string, request, render_template, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from scout import search_ending_soon, is_undervalued
from flask_sqlalchemy import SQLAlchemy
from ebaysdk.finding import Connection as Finding
import logging
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
alerts = []

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure logging
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy(app)

# Define models
class TrackedItem(db.Model):
    __tablename__ = 'tracked_items'
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    upc = db.Column(db.String, nullable=True)
    ean = db.Column(db.String, nullable=True)
    gtin = db.Column(db.String, nullable=True)
    category_id = db.Column(db.String, nullable=True)
    last_checked = db.Column(db.DateTime, nullable=False)

class BuyItNowAverage(db.Model):
    __tablename__ = 'buy_it_now_averages'
    item_type = db.Column(db.String, primary_key=True)
    average_price = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

def poll_ebay():
    global alerts
    new = []
    for item in search_ending_soon():
        if is_undervalued(item):
            new.append({
                "title": item.title,
                "price": item.price.value,
                "url": item.item_web_url
            })
    alerts = new  # simple overwrite; you can append/dedupe instead

scheduler = BackgroundScheduler()
scheduler.add_job(poll_ebay, "interval", minutes=5)
scheduler.start()

# Replace with your eBay API credentials
EBAY_APP_ID = "YourEbayAppID"

@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('query')
        logging.debug(f"Search query received: {query}")

        if query:
            try:
                # Connect to eBay API
                api = Finding(appid=EBAY_APP_ID, config_file=None)
                response = api.execute('findItemsByKeywords', {'keywords': query})
                items = response.reply.searchResult.item
                logging.debug(f"eBay API response: {items}")

                # Render the results on the index page
                return render_template('index.html', results=items)
            except Exception as e:
                logging.error(f"Error fetching eBay data: {e}")
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
        # Fetch item details from eBay API
        api = Finding(appid=EBAY_APP_ID, config_file=None)
        response = api.execute('findItemsByItemID', {'itemID': item_id})
        item = response.reply.item[0]

        # Extract relevant details
        title = item.title
        price = item.sellingStatus.currentPrice.value
        url = item.viewItemURL
        upc = item.productId.value if hasattr(item, 'productId') else None

        # Add to database
        tracked_item = TrackedItem(title=title, price=price, url=url, upc=upc)
        db.session.add(tracked_item)
        db.session.commit()

        logging.debug(f"Item added to tracking: {tracked_item}")
        return redirect('/listings')
    except Exception as e:
        logging.error(f"Error adding item to tracking: {e}")
        return redirect('/', error="Failed to add item to tracking.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
