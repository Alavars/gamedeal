import React from 'react';
import { Star, ExternalLink } from 'lucide-react';
import GameImage from './GameImage';

export default function GameCard({
  game,
  isWishlisted,
  onToggleWishlist,
  onOpenDetails,
  user,
}) {
  const title = game.external || game.title || 'Unknown Game';
  const dealId = game.cheapestDealID || game.dealID;
  const storeName = game.cheapest_store_name || game.store_name || 'Store';
  const price = game.cheapest || game.salePrice || 'N/A';
  const thumb = game.thumb || game.thumb_url || '';

  const dealUrl = dealId
    ? `https://www.cheapshark.com/redirect?dealID=${dealId}`
    : '#';

  return (
    <div className="bg-zinc-900/60 backdrop-blur-md rounded-xl shadow-lg hover:shadow-zinc-900/80 transition-all duration-300 border border-zinc-800/80 hover:border-zinc-600 overflow-hidden flex relative group">
      {/* Thumbnail */}
      <div className="w-32 h-32 flex-none bg-zinc-950 overflow-hidden">
        <GameImage
          src={thumb}
          alt={title}
          className="w-full h-full object-cover grayscale-[25%] group-hover:grayscale-0 transition-all duration-300"
          containerClassName="w-full h-full border-r border-zinc-800/80"
          iconSize="w-7 h-7"
        />
      </div>

      {/* Info */}
      <div className="p-4 flex flex-col justify-between w-full min-w-0">
        <div>
          <h3
            className="font-bold text-base text-zinc-100 truncate group-hover:text-white transition-colors"
            title={title}
          >
            {title}
          </h3>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-white font-extrabold text-base">
              ${price}
            </span>
            {dealId && (
              <a
                href={dealUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-zinc-400 hover:text-white underline flex items-center gap-0.5 truncate transition-colors"
              >
                <span>via {storeName}</span>
                <ExternalLink className="w-3 h-3 flex-none" />
              </a>
            )}
          </div>
        </div>

        <button
          onClick={() => onOpenDetails(game.gameID || game.id || game.external_id)}
          className="mt-3 w-full text-xs font-semibold py-2 rounded-lg bg-zinc-800/80 hover:bg-white hover:text-black text-zinc-200 border border-zinc-700/60 transition-all duration-200 cursor-pointer text-center"
        >
          View Details & Stats
        </button>
      </div>

      {/* Wishlist Star Button */}
      <button
        onClick={() => onToggleWishlist(game)}
        title={
          !user
            ? 'Login to add to Wishlist'
            : isWishlisted
            ? 'In your Wishlist'
            : 'Add to Wishlist'
        }
        className={`absolute top-2 left-2 p-1.5 rounded-full transition-all duration-200 z-10 cursor-pointer border ${
          isWishlisted
            ? 'opacity-100 text-white bg-zinc-950/90 border-zinc-600 shadow'
            : 'opacity-0 group-hover:opacity-100 text-zinc-400 hover:text-white bg-black/70 hover:bg-black border-zinc-800'
        }`}
      >
        <Star
          className="w-4 h-4"
          fill={isWishlisted ? 'currentColor' : 'none'}
        />
      </button>
    </div>
  );
}
