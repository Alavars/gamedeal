import React from 'react';

export default function Footer({ openInfoModal }) {
  return (
    <footer className="bg-zinc-950/90 border-t border-zinc-800/80 mt-auto relative z-20">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-center md:text-left">
            <span className="text-xl font-bold text-white tracking-tight">GameDealPulse</span>
            <p className="text-xs text-zinc-400 mt-1">
              Track prices, set alerts, never miss a deal.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-6">
            <button
              onClick={() => openInfoModal('privacy')}
              className="text-zinc-400 hover:text-white text-xs sm:text-sm transition-colors cursor-pointer"
            >
              Privacy Policy
            </button>
            <button
              onClick={() => openInfoModal('terms')}
              className="text-zinc-400 hover:text-white text-xs sm:text-sm transition-colors cursor-pointer"
            >
              Terms of Service
            </button>
            <button
              onClick={() => openInfoModal('contact')}
              className="text-zinc-400 hover:text-white text-xs sm:text-sm transition-colors cursor-pointer"
            >
              Contact Us
            </button>
          </div>
        </div>

        <div className="mt-6 border-t border-zinc-800/60 pt-6 flex flex-col md:flex-row justify-between items-center text-xs text-zinc-500 gap-2">
          <p>&copy; 2026 GameDealPulse. Built with React & FastAPI.</p>
          <p>
            Powered by{' '}
            <a
              href="https://www.cheapshark.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-zinc-400 hover:text-white underline font-medium"
            >
              CheapShark API
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
