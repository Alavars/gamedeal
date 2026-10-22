import React, { useState } from 'react';
import { Bookmark, Trash2, Mail, Save, Loader2 } from 'lucide-react';
import { api } from '../api';
import GameImage from './GameImage';

export default function WishlistView({
  wishlist,
  onRefresh,
  onOpenDetails,
  onTestEmail,
  emailTesting,
  onBackToSearch,
}) {
  const [updatingId, setUpdatingId] = useState(null);
  const [targetPrices, setTargetPrices] = useState({});

  const handlePriceChange = (id, val) => {
    setTargetPrices((prev) => ({ ...prev, [id]: val }));
  };

  const handleUpdate = async (item) => {
    const newPrice = targetPrices[item.id];
    if (newPrice === undefined || newPrice === '') return;
    setUpdatingId(item.id);
    try {
      await api.updateWishlist(item.id, {
        target_price: parseFloat(newPrice),
      });
      await onRefresh();
    } catch (err) {
      alert(err.message);
    } finally {
      setUpdatingId(null);
    }
  };

  const handleRemove = async (item) => {
    if (!confirm(`Remove "${item.game?.title}" from your wishlist?`)) return;
    try {
      await api.removeFromWishlist(item.id);
      await onRefresh();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 relative z-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-zinc-800 pb-5">
        <div>
          <h1 className="text-3xl font-black text-white flex items-center gap-2.5">
            <Bookmark className="w-7 h-7 text-zinc-100 fill-zinc-100" />
            <span>My Wishlist</span>
          </h1>
          <p className="text-xs sm:text-sm text-zinc-400 mt-1">
            We continuously track these games and send you an email alert when prices drop!
          </p>
        </div>

        <button
          onClick={onTestEmail}
          disabled={emailTesting}
          className="flex items-center gap-1.5 bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-xs px-3.5 py-2 rounded-xl border border-zinc-700 transition-all shadow-sm cursor-pointer disabled:opacity-50"
        >
          <Mail className="w-4 h-4" />
          <span>{emailTesting ? 'Sending alert...' : 'Send Test Alert Email'}</span>
        </button>
      </div>

      {wishlist.length === 0 ? (
        <div className="bg-zinc-900/60 backdrop-blur-md rounded-2xl p-12 text-center shadow-lg border border-zinc-800 mt-8">
          <Bookmark className="w-12 h-12 text-zinc-600 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-zinc-200">Your wishlist is empty</h3>
          <p className="text-xs sm:text-sm text-zinc-400 max-w-md mx-auto mt-1 mb-6">
            Search for your favorite games and click the star icon to track price drops automatically.
          </p>
          <button
            onClick={onBackToSearch}
            className="bg-white hover:bg-zinc-200 text-black font-bold text-xs sm:text-sm px-5 py-2.5 rounded-xl transition-colors cursor-pointer shadow-sm"
          >
            Find Games to Track
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
          {wishlist.map((item) => {
            const currentInput =
              targetPrices[item.id] !== undefined
                ? targetPrices[item.id]
                : item.target_price || '';

            return (
              <div
                key={item.id}
                className="bg-zinc-900/70 backdrop-blur-md rounded-2xl shadow-md border border-zinc-800/90 p-4 flex gap-4 items-center justify-between hover:border-zinc-700 transition-colors"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-16 h-16 rounded-xl flex-none bg-zinc-950 border border-zinc-800 overflow-hidden">
                    <GameImage
                      src={item.game?.thumb_url}
                      alt={item.game?.title}
                      className="w-full h-full object-cover"
                      containerClassName="w-full h-full"
                      iconSize="w-5 h-5"
                    />
                  </div>
                  <div className="min-w-0">
                    <h3
                      className="font-bold text-base text-zinc-100 truncate"
                      title={item.game?.title}
                    >
                      {item.game?.title}
                    </h3>

                    {/* Target Price input */}
                    <div className="mt-2 flex items-center gap-2">
                      <span className="text-xs text-zinc-400 flex-none">Alert below:</span>
                      <div className="relative flex items-center">
                        <span className="absolute left-2 text-xs text-zinc-500">$</span>
                        <input
                          type="number"
                          step="0.01"
                          placeholder="Price"
                          value={currentInput}
                          onChange={(e) => handlePriceChange(item.id, e.target.value)}
                          className="w-20 pl-5 pr-1 py-1 text-xs rounded-lg bg-zinc-950 border border-zinc-700 text-white focus:outline-hidden focus:ring-1 focus:ring-zinc-400"
                        />
                      </div>
                      <button
                        onClick={() => handleUpdate(item)}
                        disabled={updatingId === item.id}
                        title="Save new alert price"
                        className="p-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white border border-zinc-700 transition-colors cursor-pointer"
                      >
                        {updatingId === item.id ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <Save className="w-4 h-4" />
                        )}
                      </button>
                    </div>
                  </div>
                </div>

                <div className="flex flex-col gap-2 flex-none items-end">
                  <button
                    onClick={() => onOpenDetails(item.game?.external_id)}
                    className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-white hover:text-black text-zinc-200 border border-zinc-700 transition-all cursor-pointer"
                  >
                    View Deals
                  </button>

                  <button
                    onClick={() => handleRemove(item)}
                    className="p-1.5 rounded-lg text-zinc-500 hover:text-red-400 hover:bg-zinc-800 transition-colors cursor-pointer"
                    title="Remove from wishlist"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
