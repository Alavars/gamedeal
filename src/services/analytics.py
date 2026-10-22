import pandas as pd
from typing import List, Dict

def calculate_game_stats(deals: List[Dict]) -> Dict:
    empty_stats = {
        "min_price": 0.0,
        "max_price": 0.0,
        "avg_price": 0.0,
        "avg_discount": 0.0,
        "max_discount": 0.0,
        "max_savings_pct": 0.0
    }
    if not deals:
        return empty_stats
        
    df = pd.DataFrame(deals)
    
    if 'price' not in df.columns or 'retailPrice' not in df.columns:
        return empty_stats
        
    # Ensure types
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['retailPrice'] = pd.to_numeric(df['retailPrice'], errors='coerce').fillna(0)
    
    # Calculate discount percentage
    mask = df['retailPrice'] > 0
    df.loc[mask, 'discount'] = ((df.loc[mask, 'retailPrice'] - df.loc[mask, 'price']) / df.loc[mask, 'retailPrice']) * 100
    df['discount'] = df['discount'].fillna(0)
    
    min_price = float(df['price'].min()) if not df.empty else 0.0
    max_price = float(df['retailPrice'].max()) if not df.empty else 0.0
    avg_price = float(df['price'].mean()) if not df.empty else 0.0
    max_disc = float(df['discount'].max()) if not df.empty else 0.0
    avg_disc = float(df['discount'].mean()) if not df.empty else 0.0

    return {
        "min_price": round(min_price, 2),
        "max_price": round(max_price, 2),
        "avg_price": round(avg_price, 2),
        "avg_discount": round(avg_disc, 2),
        "max_discount": round(max_disc, 2),
        "max_savings_pct": round(max_disc, 2),
    }
