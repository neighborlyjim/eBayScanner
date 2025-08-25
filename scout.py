# scout.py
from datetime import datetime, timedelta, timezone
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import config

def search_ending_soon(limit=25):
    # Adjusted to use the Finding API instead of Browse API
    try:
        api = Finding(appid=config.APP_ID, siteid="EBAY-US", api_version="1.13.0", config_file=None, domain="svcs.sandbox.ebay.com")
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        soon = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat().replace('+00:00', 'Z')
        resp = api.execute("findItemsAdvanced", {
            "keywords": "",
            "paginationInput": {"entriesPerPage": limit},
            "itemFilter": [
                {"name": "EndTimeTo", "value": soon},
                {"name": "EndTimeFrom", "value": now}
            ]
        })
        
        # Handle response structure safely
        if hasattr(resp, 'reply') and hasattr(resp.reply, 'searchResult'):
            search_result = resp.reply.searchResult
            items = search_result.item if hasattr(search_result, 'item') else []
        else:
            print("No search results found in response")
            items = []
        return items
    except ConnectionError as e:
        print("Finding API error:", e)
        return []

def search_completed(title, limit=25):
    # Legacy Finding API for completed listings
    try:
        api = Finding(appid=config.APP_ID, siteid="EBAY-US", api_version="1.13.0", config_file=None, domain="svcs.sandbox.ebay.com")
        resp = api.execute("findCompletedItems", {
            "keywords": title,
            "paginationInput": {"entriesPerPage": limit}
        })
        
        # Handle response structure safely
        if hasattr(resp, 'reply') and hasattr(resp.reply, 'searchResult'):
            search_result = resp.reply.searchResult
            items = search_result.item if hasattr(search_result, 'item') else []
        else:
            items = []
        return [float(i.sellingStatus.currentPrice.value) for i in items]
    except ConnectionError as e:
        print("Finding API error:", e)
        return []

def is_undervalued(item, ratio=config.UNDERVALUE_RATIO):
    title = item.title
    current = float(item.price.value)
    comps = search_completed(title)
    avg = sum(comps)/len(comps) if comps else 0
    return avg and current < avg * ratio

if __name__ == "__main__":
    for it in search_ending_soon():
        if is_undervalued(it):
            print(f"🔥 {it.title}: ${it.price.value} vs avg ${(sum(search_completed(it.title))/len(search_completed(it.title))):.2f}")
