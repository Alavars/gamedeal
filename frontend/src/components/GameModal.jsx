import React, { useState, useEffect } from 'react';
import { X, ExternalLink, TrendingDown, Star, Loader2 } from 'lucide-react';
import { api } from '../api';
import GameImage from './GameImage';

export default function GameModal({
  gameId,
  onClose,
  user,
  isWishlisted,
  onToggleWishlist,
}) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [targetPrice, setTargetPrice] = useState('');
  const [addingWishlist, setAddingWishlist] = useState(false);

  useEffect(() => {
    if (!gameId) return;
    setLoading(true);
    setError(null);

    api
      .getGameDetails(gameId)
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [gameId]);

  if (!gameId) return null;

  const handleSaveToWishlist = async () => {
    if (!user) {
      alert('Please log in first to save games to your wishlist.');
      return;
    }
    setAddingWishlist(true);
    try {
      const info = data?.game?.info || {};
      await api.addToWishlist({
        gameID: gameId,
        title: info.title || 'Game',
        thumb: info.thumb || '',
        target_price: targetPrice ? parseFloat(targetPrice) : null,
      });
      onToggleWishlist({
        gameID: gameId,
        title: info.title,
        thumb: info.thumb,
      });
    } catch (err) {
      alert(err.message);
    } finally {
      setAddingWishlist(false);
    }
  };

  const gameInfo = data?.game?.info;
  const deals = data?.game?.deals || [];
  const stats = data?.stats || {};

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-zinc-900 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-zinc-800 text-zinc-100 relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white transition-colors z-10 cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {loading ? (
          <div className="p-16 flex flex-col items-center justify-center space-y-3">
            <Loader2 className="w-8 h-8 animate-spin text-zinc-300" />
            <p className="text-sm text-zinc-400">Loading game analytics & deals...</p>
          </div>
        ) : error ? (
          <div className="p-8 text-center">
            <p className="text-red-400 font-medium">Failed to load: {error}</p>
            <button
              onClick={onClose}
              className="mt-4 px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-sm font-semibold cursor-pointer"
            >
              Close
            </button>
          </div>
        ) : (
          <div>
            {/* Header info */}
            <div className="p-6 border-b border-zinc-800 flex gap-5 items-start">
              <div className="w-24 h-24 rounded-xl shadow-md bg-zinc-950 border border-zinc-800 overflow-hidden flex-none">
                <GameImage
                  src={gameInfo?.thumb}
                  alt={gameInfo?.title}
                  className="w-full h-full object-cover"
                  containerClassName="w-full h-full"
                  iconSize="w-6 h-6"
                />
              </div>
              <div className="min-w-0 flex-1">
                <h2 className="text-2xl font-black text-white truncate">
                  {gameInfo?.title}
                </h2>
                <div className="mt-1 flex flex-wrap items-center gap-3 text-sm text-zinc-400">
                  <span>
                    Lowest Historical Price:{' '}
                    <strong className="text-white font-bold">
                      ${data?.game?.cheapestPriceEver?.price || 'N/A'}
                    </strong>
                  </span>
                </div>

                {/* Target Price Form */}
                {user && (
                  <div className="mt-3.5 flex items-center gap-2">
                    <input
                      type="number"
                      step="0.01"
                      placeholder="Target price ($)"
                      value={targetPrice}
                      onChange={(e) => setTargetPrice(e.target.value)}
                      className="w-36 text-xs px-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-700 text-white placeholder-zinc-500 focus:outline-hidden focus:ring-1 focus:ring-zinc-400"
                    />
                    <button
                      onClick={handleSaveToWishlist}
                      disabled={addingWishlist}
                      className="flex items-center gap-1.5 bg-white hover:bg-zinc-200 text-black font-bold text-xs px-3.5 py-1.5 rounded-lg transition-colors cursor-pointer shadow-sm disabled:opacity-50"
                    >
                      <Star className="w-3.5 h-3.5 fill-black" />
                      <span>{isWishlisted ? 'Update Alert' : 'Add to Wishlist'}</span>
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Price Analytics Card */}
            {stats && Object.keys(stats).length > 0 && (
              <div className="p-6 bg-zinc-950/70 border-b border-zinc-800">
                <div className="flex items-center gap-2 text-zinc-200 font-bold mb-3">
                  <TrendingDown className="w-5 h-5 text-zinc-400" />
                  <span>Market Analytics</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
                  <div className="bg-zinc-900 p-2.5 rounded-xl border border-zinc-800">
                    <span className="text-xs text-zinc-400">Best Current</span>
                    <p className="text-lg font-bold text-white">
                      ${stats.min_price?.toFixed(2) || 'N/A'}
                    </p>
                  </div>
                  <div className="bg-zinc-900 p-2.5 rounded-xl border border-zinc-800">
                    <span className="text-xs text-zinc-400">Average Price</span>
                    <p className="text-lg font-bold text-zinc-200">
                      ${stats.avg_price?.toFixed(2) || 'N/A'}
                    </p>
                  </div>
                  <div className="bg-zinc-900 p-2.5 rounded-xl border border-zinc-800">
                    <span className="text-xs text-zinc-400">Max Discount</span>
                    <p className="text-lg font-bold text-zinc-100">
                      {stats.max_savings_pct?.toFixed(0) || '0'}%
                    </p>
                  </div>
                  <div className="bg-zinc-900 p-2.5 rounded-xl border border-zinc-800">
                    <span className="text-xs text-zinc-400">Retail Base</span>
                    <p className="text-lg font-bold text-zinc-500 line-through">
                      ${stats.max_price?.toFixed(2) || 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Store deals list */}
            <div className="p-6">
              <h3 className="font-bold text-zinc-100 text-base mb-4">
                Available Stores & Deals ({deals.length})
              </h3>
              {deals.length === 0 ? (
                <p className="text-sm text-zinc-400">No active store deals found.</p>
              ) : (
                <div className="space-y-2.5">
                  {deals.map((deal, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between p-3 rounded-xl border border-zinc-800/80 bg-zinc-950/40 hover:border-zinc-600 hover:bg-zinc-800/50 transition-colors"
                    >
                      <div>
                        <p className="font-semibold text-zinc-200 text-sm">
                          {deal.store_name || `Store #${deal.storeID}`}
                        </p>
                        <p className="text-xs text-zinc-500">
                          Retail: ${deal.retailPrice}
                        </p>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="text-right">
                          <p className="font-extrabold text-white text-base">
                            ${deal.price}
                          </p>
                          {parseFloat(deal.savings) > 0 && (
                            <span className="text-xs text-zinc-400 font-semibold">
                              -{parseFloat(deal.savings).toFixed(0)}%
                            </span>
                          )}
                        </div>

                        <a
                          href={`https://www.cheapshark.com/redirect?dealID=${deal.dealID}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-1 bg-white hover:bg-zinc-200 text-black text-xs font-bold px-3 py-2 rounded-lg transition-colors shadow-sm"
                        >
                          <span>Store</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
