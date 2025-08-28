# models.py - Database models separated for better organization
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TrackedItem(db.Model):
    """Model for tracking eBay items"""
    __tablename__ = 'tracked_items'
    
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    upc = db.Column(db.String, nullable=True)
    ean = db.Column(db.String, nullable=True)
    gtin = db.Column(db.String, nullable=True)
    category_id = db.Column(db.String, nullable=True)
    last_checked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrackedItem {self.title}>'

class BuyItNowAverage(db.Model):
    """Model for storing average prices of Buy It Now items"""
    __tablename__ = 'buy_it_now_averages'
    
    item_type = db.Column(db.String, primary_key=True)
    average_price = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BuyItNowAverage {self.item_type}: ${self.average_price}>'
