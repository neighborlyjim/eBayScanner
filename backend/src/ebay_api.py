# ebay_api.py - Centralized eBay API helper to eliminate code duplication
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import config
import logging

class EbayAPIHelper:
    """Centralized eBay API helper following DRY principles"""
    
    def __init__(self):
        self.app_id = config.APP_ID
        self.siteid = "EBAY-US"
        self.api_version = "1.13.0"
    
    def _get_api_connection(self):
        """Get a configured eBay Finding API connection"""
        return Finding(
            appid=self.app_id,
            siteid=self.siteid,
            api_version=self.api_version,
            config_file=None
        )
    
    def _execute_api_call(self, operation, parameters):
        """Execute an eBay API call with error handling"""
        try:
            api = self._get_api_connection()
            return api.execute(operation, parameters)
        except ConnectionError as e:
            logging.error(f"eBay API error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in eBay API call: {e}")
            raise
    
    def find_items_by_keywords(self, keywords, filters=None, pagination=None, sort_order=None):
        """Find items by keywords with optional filters"""
        params = {"keywords": keywords}
        
        if pagination:
            params["paginationInput"] = pagination
        
        if filters:
            params["itemFilter"] = filters
            
        if sort_order:
            params["sortOrder"] = sort_order
            
        return self._execute_api_call("findItemsByKeywords", params)
    
    def find_items_advanced(self, filters=None, pagination=None):
        """Find items using advanced search"""
        params = {"keywords": ""}
        
        if pagination:
            params["paginationInput"] = pagination
            
        if filters:
            params["itemFilter"] = filters
            
        return self._execute_api_call("findItemsAdvanced", params)
    
    def find_completed_items(self, keywords, filters=None, pagination=None):
        """Find completed/sold items"""
        params = {"keywords": keywords}
        
        if pagination:
            params["paginationInput"] = pagination
            
        if filters:
            params["itemFilter"] = filters
        else:
            params["itemFilter"] = [{"name": "SoldItemsOnly", "value": "true"}]
            
        return self._execute_api_call("findCompletedItems", params)
    
    def find_item_by_id(self, item_id):
        """Find a specific item by ID"""
        return self._execute_api_call("findItemsByItemID", {"itemID": item_id})
    
    def extract_items_from_response(self, response):
        """Extract items array from eBay API response safely"""
        if hasattr(response, 'reply') and hasattr(response.reply, 'searchResult'):
            search_result = response.reply.searchResult
            return search_result.item if hasattr(search_result, 'item') else []
        return []
    
    def extract_prices_from_items(self, items):
        """Extract prices from items array"""
        prices = []
        for item in items:
            try:
                price = float(item.sellingStatus.currentPrice.value)
                prices.append(price)
            except (AttributeError, ValueError):
                continue
        return prices

# Create global instance for use throughout the application
ebay_api = EbayAPIHelper()
