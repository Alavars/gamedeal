const API_BASE = 'http://127.0.0.1:8000';

function getHeaders() {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export const api = {
  // Auth
  async register(email, password) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');
    return data;
  },

  async login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');
    if (data.token) {
      localStorage.setItem('token', data.token);
    }
    if (data.user) {
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  async logout() {
    try {
      await fetch(`${API_BASE}/auth/logout`, { credentials: 'include' });
    } catch (_) {}
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  async getMe() {
    const token = localStorage.getItem('token');
    const cachedUser = localStorage.getItem('user');
    if (!token) return null;

    try {
      const res = await fetch(`${API_BASE}/auth/me`, {
        headers: getHeaders(),
        credentials: 'include',
      });
      if (res.status === 401 || res.status === 404) {
        // Token is genuinely invalid
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        return null;
      }
      if (res.ok) {
        const userData = await res.json();
        localStorage.setItem('user', JSON.stringify(userData));
        return userData;
      }
    } catch (err) {
      // Server is currently restarting/offline: preserve session!
      console.warn('Server offline/restarting, preserving cached login session');
    }

    if (cachedUser) {
      try {
        return JSON.parse(cachedUser);
      } catch (_) {}
    }
    return null;
  },

  // Deals
  async getTopDeals(limit = 6) {
    const res = await fetch(`${API_BASE}/deals/top?limit=${limit}`);
    if (!res.ok) throw new Error('Failed to fetch top deals');
    const data = await res.json();
    return data.deals || [];
  },

  async searchDeals(query) {
    if (!query || query.trim().length < 3) return [];
    const res = await fetch(`${API_BASE}/deals/search?query=${encodeURIComponent(query.trim())}`);
    if (!res.ok) throw new Error('Search failed');
    const data = await res.json();
    return data.results || [];
  },

  async getGameDetails(gameId) {
    const res = await fetch(`${API_BASE}/deals/${gameId}`);
    if (!res.ok) throw new Error('Failed to fetch game details');
    return res.json();
  },

  // Wishlist
  async getWishlist() {
    const res = await fetch(`${API_BASE}/wishlist`, {
      headers: getHeaders(),
      credentials: 'include',
    });
    if (!res.ok) throw new Error('Failed to fetch wishlist');
    return res.json();
  },

  async addToWishlist(game) {
    const res = await fetch(`${API_BASE}/wishlist/add`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        external_id: String(game.gameID || game.external_id),
        title: game.external || game.title,
        thumb_url: game.thumb || game.thumb_url || '',
        target_price: game.target_price ? parseFloat(game.target_price) : null,
      }),
      credentials: 'include',
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to add to wishlist');
    return data;
  },

  async removeFromWishlist(wishlistId) {
    const res = await fetch(`${API_BASE}/wishlist/${wishlistId}`, {
      method: 'DELETE',
      headers: getHeaders(),
      credentials: 'include',
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to remove item');
    return data;
  },

  async updateWishlist(wishlistId, updateData) {
    const res = await fetch(`${API_BASE}/wishlist/${wishlistId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(updateData),
      credentials: 'include',
    });
    return res.json();
  },

  async sendTestEmail() {
    const res = await fetch(`${API_BASE}/wishlist/test-email`, {
      method: 'POST',
      headers: getHeaders(),
      credentials: 'include',
    });
    return res.json();
  },

  // Info pages
  async getPrivacy() {
    const res = await fetch(`${API_BASE}/privacy`);
    return res.json();
  },

  async getTerms() {
    const res = await fetch(`${API_BASE}/terms`);
    return res.json();
  },

  async getContact() {
    const res = await fetch(`${API_BASE}/contact`);
    return res.json();
  },
};
