import pandas as pd
from typing import List, Dict

def calculate_game_stats(deals: List[Dict]) -> Dict:
    if not deals:
        return {"avg_price": 0, "avg_discount": 0, "max_discount": 0}
        
    df = pd.DataFrame(deals)
    
    if 'price' not in df.columns or 'retailPrice' not in df.columns:
        return {"avg_price": 0, "avg_discount": 0, "max_discount": 0}
        
    # Ensure types
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['retailPrice'] = pd.to_numeric(df['retailPrice'], errors='coerce').fillna(0)
    
    # Calculate discount percentage
    # Avoid division by zero
    mask = df['retailPrice'] > 0
    df.loc[mask, 'discount'] = ((df.loc[mask, 'retailPrice'] - df.loc[mask, 'price']) / df.loc[mask, 'retailPrice']) * 100
    df['discount'] = df['discount'].fillna(0)
    
    return {
        "avg_price": round(df['price'].mean(), 2),
        "avg_discount": round(df['discount'].mean(), 2),
        "max_discount": round(df['discount'].max(), 2),
    }
