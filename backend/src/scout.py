# scout.py
from datetime import datetime, timedelta, timezone
import config
from ebay_api import ebay_api
from utils import calculate_time_left, extract_model_from_title, determine_urgency, safe_get_attribute

def search_ending_soon(limit=25):
    """Search for items ending soon using centralized eBay API"""
    try:
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        soon = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat().replace('+00:00', 'Z')
        
        filters = [
            {"name": "EndTimeTo", "value": soon},
            {"name": "EndTimeFrom", "value": now}
        ]
        
        pagination = {"entriesPerPage": limit}
        
        resp = ebay_api.find_items_advanced(filters=filters, pagination=pagination)
        return ebay_api.extract_items_from_response(resp)
        
    except ConnectionError as e:
        print("Finding API error:", e)
        return []

def search_completed(title, limit=25):
    """Search for completed listings using centralized eBay API"""
    try:
        pagination = {"entriesPerPage": limit}
        resp = ebay_api.find_completed_items(title, pagination=pagination)
        items = ebay_api.extract_items_from_response(resp)
        return ebay_api.extract_prices_from_items(items)
        
    except ConnectionError as e:
        print("Finding API error:", e)
        return []

def is_undervalued(item, ratio=config.UNDERVALUE_RATIO):
    title = item.title
    current = float(item.price.value)
    comps = search_completed(title)
    avg = sum(comps)/len(comps) if comps else 0
    return avg and current < avg * ratio

def search_undervalued_deals(query, max_price=1000, max_time_hours=24, limit=50):
    """Search for undervalued deals on eBay with price and time filters using centralized API"""
    try:
        # Calculate time range
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(hours=max_time_hours)
        
        # Build search parameters using centralized API
        filters = [
            {"name": "MaxPrice", "value": max_price, "paramName": "Currency", "paramValue": "USD"},
            {"name": "EndTimeTo", "value": end_time.isoformat().replace('+00:00', 'Z')},
            {"name": "ListingType", "value": "Auction"},  # Focus on auctions for better deals
            {"name": "Condition", "value": ["New", "Used"]},
        ]
        
        pagination = {"entriesPerPage": limit}
        sort_order = "PricePlusShippingLowest"
        
        resp = ebay_api.find_items_by_keywords(
            keywords=query,
            filters=filters,
            pagination=pagination,
            sort_order=sort_order
        )
        
        deals = []
        items = ebay_api.extract_items_from_response(resp)
        
        for item in items:
            try:
                # Extract item details
                current_price = float(item.sellingStatus.currentPrice.value)
                
                # Skip if over max price
                if current_price > max_price:
                    continue
                    
                # Calculate time left
                end_time = item.listingInfo.endTime
                time_left = calculate_time_left(end_time)
                
                # Get completed listings for price comparison
                avg_sold_price = get_average_sold_price(item.title)
                
                # Calculate savings and discount
                if avg_sold_price and avg_sold_price > current_price:
                    savings = avg_sold_price - current_price
                    discount = int((savings / avg_sold_price) * 100)
                    
                    # Only include if it's a good deal (>20% savings)
                    if discount >= 20:
                        urgency = determine_urgency(time_left)
                        
                        deal = {
                            "title": item.title,
                            "currentPrice": current_price,
                            "avgSoldPrice": avg_sold_price,
                            "discount": discount,
                            "savings": savings,
                            "condition": safe_get_attribute(item, 'condition.conditionDisplayName', 'Unknown'),
                            "location": safe_get_attribute(item, 'location', 'Unknown'),
                            "itemUrl": item.viewItemURL,
                            "imageUrl": safe_get_attribute(item, 'galleryURL', ''),
                            "soldCount": 10,  # Placeholder - you'd get this from completed search
                            "model": extract_model_from_title(item.title),
                            "listingType": item.listingInfo.listingType,
                            "timeLeft": time_left,
                            "bidCount": int(safe_get_attribute(item, 'sellingStatus.bidCount', 0)),
                            "urgency": urgency
                        }
                        deals.append(deal)
            except Exception as e:
                print(f"Error processing item: {e}")
                continue
                
        return deals[:20]  # Return top 20 deals
        
    except ConnectionError as e:
        print("eBay API error:", e)
        # Return demo data when API fails due to invalid credentials
        return get_demo_deals(query, max_price)
    except Exception as e:
        print("Search error:", e)
        # Return demo data when API fails due to invalid credentials
        return get_demo_deals(query, max_price)

def get_demo_deals(query, max_price=1000):
    """Return demo deals for testing when eBay API is not available"""
    demo_deals = [
        {
            "title": f"{query.capitalize()} D3500 DSLR Camera with 18-55mm VR Lens - Excellent Condition",
            "currentPrice": 89.99,
            "avgSoldPrice": 129.99,
            "discount": 31,
            "savings": 40.00,
            "condition": "Excellent",
            "location": "California, US",
            "itemUrl": "https://ebay.com/demo-item-1",
            "imageUrl": "https://i.ebayimg.com/images/g/demo1.jpg",
            "soldCount": 15,
            "model": f"{query.upper()} D3500",
            "listingType": "Auction",
            "timeLeft": "2h 15m",
            "bidCount": 3,
            "urgency": "high"
        },
        {
            "title": f"Vintage {query.capitalize()} FE 35mm Film Camera - Working Condition",
            "currentPrice": 45.50,
            "avgSoldPrice": 75.00,
            "discount": 39,
            "savings": 29.50,
            "condition": "Good",
            "location": "New York, US",
            "itemUrl": "https://ebay.com/demo-item-2",
            "imageUrl": "https://i.ebayimg.com/images/g/demo2.jpg",
            "soldCount": 8,
            "model": f"{query.upper()} FE",
            "listingType": "Auction",
            "timeLeft": "45 minutes",
            "bidCount": 7,
            "urgency": "critical"
        },
        {
            "title": f"{query.capitalize()} 50mm f/1.8 Prime Lens - Like New in Box",
            "currentPrice": 156.00,
            "avgSoldPrice": 199.99,
            "discount": 22,
            "savings": 43.99,
            "condition": "New",
            "location": "Texas, US",
            "itemUrl": "https://ebay.com/demo-item-3",
            "imageUrl": "https://i.ebayimg.com/images/g/demo3.jpg",
            "soldCount": 25,
            "model": f"{query.upper()} 50mm",
            "listingType": "Auction",
            "timeLeft": "5h 30m",
            "bidCount": 12,
            "urgency": "high"
        },
        {
            "title": f"Professional {query.capitalize()} Flash Speedlight - Barely Used",
            "currentPrice": 78.25,
            "avgSoldPrice": 120.00,
            "discount": 35,
            "savings": 41.75,
            "condition": "Excellent",
            "location": "Florida, US",
            "itemUrl": "https://ebay.com/demo-item-4",
            "imageUrl": "https://i.ebayimg.com/images/g/demo4.jpg",
            "soldCount": 18,
            "model": f"{query.upper()} SB-700",
            "listingType": "Auction",
            "timeLeft": "1h 22m",
            "bidCount": 5,
            "urgency": "critical"
        }
    ]
    
    # Filter by max price
    filtered_deals = [deal for deal in demo_deals if deal["currentPrice"] <= max_price]
    return filtered_deals

def get_average_sold_price(title, limit=20):
    """Get average sold price for similar items using centralized API"""
    try:
        pagination = {"entriesPerPage": limit}
        resp = ebay_api.find_completed_items(title, pagination=pagination)
        items = ebay_api.extract_items_from_response(resp)
        prices = ebay_api.extract_prices_from_items(items)
        return sum(prices) / len(prices) if prices else None
        
    except Exception as e:
        print(f"Error getting sold prices: {e}")
        return None


