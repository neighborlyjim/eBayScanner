import { useState } from 'react';
import { Search, Camera, TrendingDown, DollarSign, ExternalLink, AlertCircle, RefreshCw, Info, Clock, Filter } from 'lucide-react';
import './App.css';

interface Deal {
  title: string;
  currentPrice: number;
  avgSoldPrice: number;
  discount: number;
  savings: number;
  condition: string;
  location: string;
  itemUrl: string;
  imageUrl: string;
  soldCount: number;
  model: string;
  listingType: string;
  timeLeft: string;
  bidCount: number;
  urgency: string;
}

const EbayCameraAnalyzer = () => {
  const [searchQuery, setSearchQuery] = useState('iPhone 15');
  const [maxPrice, setMaxPrice] = useState(300);
  const [maxTimeHours, setMaxTimeHours] = useState(1);
  const [searchResults, setSearchResults] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const searchEbayDeals = async () => {
    setLoading(true);
    setError('');
    setSearchResults([]);

    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: searchQuery,
          maxPrice: maxPrice,
          maxTimeHours: maxTimeHours
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      setSearchResults(data.results || []);
      setLoading(false);
    } catch (err) {
      console.error('Search error:', err);
      setError((err as Error).message || 'Failed to search eBay listings');
      setLoading(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Camera className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">eBay Deal Finder</h1>
                <p className="text-gray-600 text-sm">Find undervalued items on eBay across all categories</p>
              </div>
            </div>
          </div>

          {/* Important Notice */}
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-start gap-2">
              <Info className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-green-900 font-medium mb-1">Live eBay Integration:</p>
                <p className="text-green-800 text-sm">
                  This app searches real eBay auctions using your Developer API credentials. 
                  Find deals on electronics, collectibles, fashion, cars, and more!
                </p>
              </div>
            </div>
          </div>

          {/* Filter Controls */}
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center gap-2 mb-4">
              <Filter className="h-5 w-5 text-blue-600" />
              <h3 className="text-blue-900 font-semibold">Search Filters</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-blue-900 mb-2">
                  <DollarSign className="h-4 w-4 inline mr-1" />
                  Maximum Price
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min="50"
                    max="1000"
                    step="50"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(parseInt(e.target.value))}
                    className="flex-1"
                  />
                  <div className="bg-white border border-blue-300 rounded px-3 py-1 font-medium text-blue-900 min-w-[80px] text-center">
                    ${maxPrice}
                  </div>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-900 mb-2">
                  <Clock className="h-4 w-4 inline mr-1" />
                  Maximum Time Left (hours)
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min="0.5"
                    max="24"
                    step="0.5"
                    value={maxTimeHours}
                    onChange={(e) => setMaxTimeHours(parseFloat(e.target.value))}
                    className="flex-1"
                  />
                  <div className="bg-white border border-blue-300 rounded px-3 py-1 font-medium text-blue-900 min-w-[80px] text-center">
                    {maxTimeHours}h
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Search Controls */}
          <div className="flex gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search anything (e.g., iPhone 15, PlayStation 5, Nike shoes, vintage camera)"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
              />
            </div>
            <button
              onClick={searchEbayDeals}
              disabled={loading || !searchQuery.trim()}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2 transition-colors text-lg font-medium"
            >
              {loading ? (
                <>
                  <RefreshCw className="h-5 w-5 animate-spin" />
                  Searching...
                </>
              ) : (
                <>
                  <Search className="h-5 w-5" />
                  Search eBay
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-red-600" />
              <span className="text-red-700">{error}</span>
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-16">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-xl text-gray-700 mb-2">Searching eBay for "{searchQuery}" under ${maxPrice} ending within {maxTimeHours}h...</p>
            <p className="text-gray-600">Finding real deals using eBay API</p>
          </div>
        )}

        {/* Results */}
        {searchResults.length > 0 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <TrendingDown className="h-6 w-6 text-green-600" />
                💰 {searchResults.length} Deal{searchResults.length !== 1 ? 's' : ''} Found Under ${maxPrice}!
              </h2>
              <div className="text-right">
                <p className="text-sm text-gray-600">Live eBay results • Max ${maxPrice} • Within {maxTimeHours}h</p>
              </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {searchResults.map((deal, index) => (
                <div key={index} className="bg-white rounded-xl shadow-sm border hover:shadow-lg transition-shadow duration-300">
                  <div className="p-6">
                    {/* Deal Badge with Urgency */}
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex flex-col gap-1">
                        <span className="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-semibold bg-green-100 text-green-800">
                          {deal.discount}% OFF
                        </span>
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          deal.urgency === 'critical' 
                            ? 'bg-red-100 text-red-800 animate-pulse' 
                            : 'bg-orange-100 text-orange-800'
                        }`}>
                          🔥 {deal.timeLeft} left
                        </span>
                      </div>
                      <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                        Demo #{index + 1}
                      </span>
                    </div>

                    {/* Placeholder for Image */}
                    <div className="mb-4 h-48 bg-gray-200 rounded-lg flex items-center justify-center">
                      <Camera className="h-12 w-12 text-gray-400" />
                    </div>

                    {/* Title */}
                    <h3 className="font-semibold text-gray-900 mb-4 text-lg leading-tight">
                      {deal.title}
                    </h3>

                    {/* Pricing Details */}
                    <div className="space-y-3 mb-4">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Current Price:</span>
                        <span className="font-bold text-xl text-blue-600">
                          {formatPrice(deal.currentPrice)}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Average Sold:</span>
                        <span className="text-gray-900 line-through">
                          {formatPrice(deal.avgSoldPrice)}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center pt-2 border-t border-gray-100">
                        <span className="text-gray-700 font-medium">You Save:</span>
                        <span className="font-bold text-lg text-green-600">
                          {formatPrice(deal.savings)}
                        </span>
                      </div>
                    </div>

                    {/* Details */}
                    <div className="space-y-2 text-sm mb-4">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Type:</span>
                        <span className="font-medium text-blue-600">{deal.listingType}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Time Left:</span>
                        <span className={`font-bold ${
                          deal.urgency === 'critical' ? 'text-red-600' : 'text-orange-600'
                        }`}>
                          ⏰ {deal.timeLeft}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Current Bids:</span>
                        <span className="text-gray-900 font-medium">{deal.bidCount} bids</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Model:</span>
                        <span className="font-medium">{deal.model}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Condition:</span>
                        <span className="text-gray-900">{deal.condition}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Location:</span>
                        <span className="text-gray-900">{deal.location}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Analysis based on:</span>
                        <span className="text-gray-900">{deal.soldCount} sold items</span>
                      </div>
                    </div>

                    {/* CTA Button with Urgency */}
                    <a
                      href={deal.itemUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={`w-full py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2 font-medium ${
                        deal.urgency === 'critical'
                          ? 'bg-red-600 text-white hover:bg-red-700 animate-pulse'
                          : 'bg-blue-600 text-white hover:bg-blue-700'
                      }`}
                    >
                      <ExternalLink className="h-4 w-4" />
                      {deal.urgency === 'critical' ? 'BID NOW!' : 'Place Bid'}
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {searchResults.length === 0 && !loading && (
          <div className="text-center py-16">
            <Camera className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <p className="text-xl text-gray-600 mb-2">Ready to find real eBay deals!</p>
            <p className="text-gray-500">Enter any search term and click "Search eBay" to find undervalued items.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EbayCameraAnalyzer;
