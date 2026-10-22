import React, { useState, useEffect, useRef } from 'react';
import { Search, Loader2, Sparkles, TrendingUp, X } from 'lucide-react';
import { api } from './api';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import GameCard from './components/GameCard';
import GameModal from './components/GameModal';
import AuthModal from './components/AuthModal';
import InfoModal from './components/InfoModal';
import WishlistView from './components/WishlistView';
import CipherReach from './components/originkit/ui/two-reaching-hands';

export default function App() {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('user');
      return saved ? JSON.parse(saved) : null;
    } catch (_) {
      return null;
    }
  });
  const [wishlist, setWishlist] = useState([]);
  const [topDeals, setTopDeals] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [loadingTop, setLoadingTop] = useState(true);
  const [currentView, setCurrentView] = useState('home'); // 'home' | 'wishlist'
  const [activeGameId, setActiveGameId] = useState(null);
  const [authModal, setAuthModal] = useState({ isOpen: false, mode: 'login' });
  const [infoModalType, setInfoModalType] = useState(null);
  const [emailTesting, setEmailTesting] = useState(false);

  const debounceTimer = useRef(null);

  // Check if search is active
  const isSearchActive = searchQuery.trim().length > 0;

  // Initial user & top deals fetch
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      loadWishlist();
    }

    api.getMe().then((u) => {
      if (u) {
        setUser(u);
        loadWishlist();
      } else {
        setUser(null);
      }
    });

    api
      .getTopDeals(6)
      .then((deals) => setTopDeals(deals))
      .catch((err) => console.error('Error loading top deals:', err))
      .finally(() => setLoadingTop(false));
  }, []);

  const loadWishlist = async () => {
    try {
      const items = await api.getWishlist();
      setWishlist(items);
    } catch (err) {
      console.error('Failed to load wishlist:', err);
    }
  };

  // Debounced search
  useEffect(() => {
    if (debounceTimer.current) clearTimeout(debounceTimer.current);

    if (!searchQuery || searchQuery.trim().length < 3) {
      setSearchResults([]);
      setSearching(false);
      return;
    }

    setSearching(true);
    debounceTimer.current = setTimeout(() => {
      api
        .searchDeals(searchQuery)
        .then((res) => setSearchResults(res))
        .catch((err) => console.error('Search error:', err))
        .finally(() => setSearching(false));
    }, 600);

    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
    };
  }, [searchQuery]);

  // Wishlist toggle handler
  const isWishlisted = (game) => {
    const targetId = String(game.gameID || game.id || game.external_id);
    return wishlist.some(
      (item) => String(item.game?.external_id) === targetId || String(item.game_id) === targetId
    );
  };

  const handleToggleWishlist = async (game) => {
    if (!user) {
      setAuthModal({ isOpen: true, mode: 'login' });
      return;
    }

    const targetId = String(game.gameID || game.id || game.external_id);
    const existing = wishlist.find(
      (item) => String(item.game?.external_id) === targetId
    );

    if (existing) {
      try {
        await api.removeFromWishlist(existing.id);
        setWishlist((prev) => prev.filter((i) => i.id !== existing.id));
      } catch (err) {
        alert(err.message);
      }
    } else {
      try {
        await api.addToWishlist(game);
        await loadWishlist();
      } catch (err) {
        alert(err.message);
      }
    }
  };

  const handleLogout = async () => {
    await api.logout();
    setUser(null);
    setWishlist([]);
    if (currentView === 'wishlist') setCurrentView('home');
  };

  const handleTestEmail = async () => {
    setEmailTesting(true);
    try {
      const res = await api.sendTestEmail();
      alert(res.message || 'Test email sent! Check your inbox or console.');
    } catch (err) {
      alert(err.message);
    } finally {
      setEmailTesting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col relative bg-[#09090b] text-zinc-100 overflow-x-hidden selection:bg-zinc-800 selection:text-white">
      {/* Originkit "Two Reaching Hands" Backdrop Artwork on Search Page */}
      {currentView === 'home' && (
        <div
          className={`fixed inset-0 z-0 pointer-events-none transition-all duration-700 ease-in-out ${
            isSearchActive
              ? 'opacity-15 blur-xl scale-95'
              : 'opacity-85 blur-0 scale-100'
          }`}
          style={{
            filter: isSearchActive ? 'blur(18px)' : 'none',
            transform: isSearchActive ? 'scale(0.96)' : 'scale(1)',
            transition: 'filter 0.7s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1), transform 0.7s cubic-bezier(0.4, 0, 0.2, 1)',
          }}
        >
          <CipherReach
            background="#09090b"
            glyphColor="#f4f4f5"
            accent="#ffffff"
            accentAmount={20}
            columns={79}
            scale={92}
            look={{
              dotColor: '#141416',
              dotSize: 14,
              glyphSize: 92,
              squareSize: 67,
              glow: 15,
              bevel: 18,
              vignette: 30,
              darkLevel: 25,
              midLevel: 75,
            }}
          />
        </div>
      )}

      {/* Navigation */}
      <Navbar
        user={user}
        currentView={currentView}
        setCurrentView={setCurrentView}
        openAuthModal={(mode) => setAuthModal({ isOpen: true, mode })}
        onLogout={handleLogout}
        onTestEmail={handleTestEmail}
        emailTesting={emailTesting}
      />

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 flex-1 w-full relative z-10">
        {currentView === 'wishlist' ? (
          <WishlistView
            wishlist={wishlist}
            onRefresh={loadWishlist}
            onOpenDetails={(id) => setActiveGameId(id)}
            onTestEmail={handleTestEmail}
            emailTesting={emailTesting}
            onBackToSearch={() => setCurrentView('home')}
          />
        ) : (
          <div>
            {/* Search Header */}
            <div className="max-w-2xl mx-auto text-center mb-10 pt-4">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-medium bg-zinc-900/90 border border-zinc-800 text-zinc-300 mb-4 backdrop-blur-md">
                <Sparkles className="w-3.5 h-3.5 text-zinc-100" />
                Live Deal Tracker
              </span>
              <h1 className="text-4xl sm:text-5xl font-black text-white tracking-tight">
                Find the Best PC Game Deals
              </h1>
              <p className="mt-3 text-sm sm:text-base text-zinc-400">
                Track historical prices across 30+ stores and get notified when games hit your target price.
              </p>

              {/* Reactive Search Box */}
              <div className="mt-8 relative max-w-xl mx-auto">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-zinc-400">
                  <Search className="w-5 h-5" />
                </div>
                <input
                  type="text"
                  placeholder="Search games (e.g., Witcher 3, Cyberpunk, Elden Ring)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-11 pr-11 py-3.5 bg-zinc-900/80 backdrop-blur-md border border-zinc-700/80 rounded-2xl shadow-xl text-sm text-white placeholder-zinc-500 focus:outline-hidden focus:ring-2 focus:ring-zinc-400 focus:border-zinc-400 transition-all"
                />
                {searchQuery && !searching && (
                  <button
                    onClick={() => setSearchQuery('')}
                    className="absolute inset-y-0 right-0 pr-4 flex items-center text-zinc-400 hover:text-white cursor-pointer"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
                {searching && (
                  <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
                    <Loader2 className="w-5 h-5 animate-spin text-zinc-300" />
                  </div>
                )}
              </div>
            </div>

            {/* Results or Top Deals */}
            {searchQuery.trim().length >= 3 ? (
              <div className="backdrop-blur-xs rounded-2xl p-2 transition-all">
                <div className="flex items-center justify-between mb-6 border-b border-zinc-800/80 pb-3">
                  <h2 className="text-2xl font-bold text-white">
                    Search Results for "{searchQuery}"
                  </h2>
                  <span className="text-xs font-semibold text-zinc-400">
                    {searchResults.length} games found
                  </span>
                </div>

                {searching && searchResults.length === 0 ? (
                  <div className="py-16 text-center">
                    <Loader2 className="w-8 h-8 animate-spin text-zinc-300 mx-auto mb-2" />
                    <p className="text-sm text-zinc-400">Searching deals across all stores...</p>
                  </div>
                ) : searchResults.length === 0 ? (
                  <div className="bg-zinc-900/70 backdrop-blur-md rounded-2xl p-12 text-center shadow-lg border border-zinc-800">
                    <p className="text-zinc-400 font-medium">
                      No games found matching "{searchQuery}". Try another title!
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {searchResults.map((game) => (
                      <GameCard
                        key={game.gameID}
                        game={game}
                        isWishlisted={isWishlisted(game)}
                        onToggleWishlist={handleToggleWishlist}
                        onOpenDetails={(id) => setActiveGameId(id)}
                        user={user}
                      />
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div>
                <div className="flex items-center gap-2 mb-6 border-b border-zinc-800/80 pb-3">
                  <TrendingUp className="w-5 h-5 text-zinc-200" />
                  <h2 className="text-xl sm:text-2xl font-black text-white">
                    New & Trending Deals
                  </h2>
                </div>

                {loadingTop ? (
                  <div className="py-16 text-center">
                    <Loader2 className="w-8 h-8 animate-spin text-zinc-300 mx-auto mb-2" />
                    <p className="text-sm text-zinc-400">Fetching latest discounts...</p>
                  </div>
                ) : topDeals.length === 0 ? (
                  <div className="bg-zinc-900/60 backdrop-blur-md rounded-2xl p-12 text-center shadow-lg border border-zinc-800">
                    <p className="text-zinc-400">No deals currently available.</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {topDeals.map((game) => (
                      <GameCard
                        key={game.gameID}
                        game={game}
                        isWishlisted={isWishlisted(game)}
                        onToggleWishlist={handleToggleWishlist}
                        onOpenDetails={(id) => setActiveGameId(id)}
                        user={user}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <Footer openInfoModal={(type) => setInfoModalType(type)} />

      {/* Modals */}
      {activeGameId && (
        <GameModal
          gameId={activeGameId}
          onClose={() => setActiveGameId(null)}
          user={user}
          isWishlisted={isWishlisted({ gameID: activeGameId })}
          onToggleWishlist={handleToggleWishlist}
        />
      )}

      <AuthModal
        isOpen={authModal.isOpen}
        initialMode={authModal.mode}
        onClose={() => setAuthModal({ isOpen: false, mode: 'login' })}
        onAuthSuccess={(u) => {
          setUser(u);
          loadWishlist();
        }}
      />

      <InfoModal
        type={infoModalType}
        onClose={() => setInfoModalType(null)}
      />
    </div>
  );
}
