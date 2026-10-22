import React from 'react';
import { Bookmark, LogIn, LogOut, UserPlus, Mail, Flame } from 'lucide-react';

export default function Navbar({
  user,
  currentView,
  setCurrentView,
  openAuthModal,
  onLogout,
  onTestEmail,
  emailTesting,
}) {
  return (
    <nav className="bg-zinc-950/80 backdrop-blur-md border-b border-zinc-800/80 text-zinc-100 sticky top-0 z-30 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo & Main Nav */}
          <div className="flex items-center space-x-6">
            <button
              onClick={() => setCurrentView('home')}
              className="flex items-center space-x-2 text-xl sm:text-2xl font-black tracking-tight text-white hover:text-zinc-200 transition-colors cursor-pointer"
            >
              <Flame className="w-6 h-6 text-zinc-100 fill-zinc-100" />
              <span>GameDealPulse</span>
            </button>
            <button
              onClick={() => setCurrentView('home')}
              className={`text-xs sm:text-sm font-semibold px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                currentView === 'home'
                  ? 'bg-zinc-800 text-white border border-zinc-700'
                  : 'text-zinc-400 hover:text-white hover:bg-zinc-900'
              }`}
            >
              Search Games
            </button>
          </div>

          {/* User actions */}
          <div className="flex items-center space-x-2.5">
            {user ? (
              <>
                <button
                  onClick={() => setCurrentView('wishlist')}
                  className={`flex items-center space-x-1.5 text-xs sm:text-sm font-semibold px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                    currentView === 'wishlist'
                      ? 'bg-zinc-800 text-white border border-zinc-700'
                      : 'text-zinc-400 hover:text-white hover:bg-zinc-900'
                  }`}
                >
                  <Bookmark className="w-4 h-4" />
                  <span>My Wishlist</span>
                </button>

                <button
                  onClick={onTestEmail}
                  disabled={emailTesting}
                  title="Send a sample price alert to your email"
                  className="hidden sm:flex items-center space-x-1.5 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 hover:text-white text-xs font-medium px-3 py-1.5 rounded-lg border border-zinc-800 transition-colors cursor-pointer disabled:opacity-50"
                >
                  <Mail className="w-3.5 h-3.5" />
                  <span>{emailTesting ? 'Sending...' : 'Test Email'}</span>
                </button>

                <div className="hidden md:flex items-center text-xs text-zinc-400 bg-zinc-900/90 border border-zinc-800/80 px-2.5 py-1.5 rounded-lg">
                  <span className="truncate max-w-[150px]">{user.email}</span>
                </div>

                <button
                  onClick={onLogout}
                  className="flex items-center space-x-1.5 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 hover:text-red-400 border border-zinc-800 text-xs sm:text-sm font-medium px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => openAuthModal('login')}
                  className="flex items-center space-x-1 text-xs sm:text-sm font-medium text-zinc-300 hover:text-white px-3 py-1.5 transition-colors cursor-pointer"
                >
                  <LogIn className="w-4 h-4" />
                  <span>Login</span>
                </button>
                <button
                  onClick={() => openAuthModal('register')}
                  className="flex items-center space-x-1 bg-white hover:bg-zinc-200 text-zinc-950 text-xs sm:text-sm font-bold px-3.5 py-1.5 rounded-lg transition-colors shadow-sm cursor-pointer"
                >
                  <UserPlus className="w-4 h-4" />
                  <span>Register</span>
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
