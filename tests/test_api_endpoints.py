import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_api():
    print("1. Testing GET / (Root)")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert "endpoints" in data
    print("   Root API OK:", data["app"])

    print("2. Testing CORS headers")
    res = client.options(
        "/deals/search",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert res.status_code == 200
    assert res.headers.get("access-control-allow-origin") == "http://localhost:5173"
    print("   CORS preflight OK")

    print("3. Testing Auth: Register & Login")
    test_email = "react_test_user@example.com"
    test_pass = "secure12345"

    # Register
    res = client.post("/auth/register", json={"email": test_email, "password": test_pass})
    assert res.status_code in [201, 400], f"Unexpected status: {res.status_code}"
    print("   Register status:", res.status_code)

    # Login
    res = client.post("/auth/login", json={"email": test_email, "password": test_pass})
    assert res.status_code == 200
    login_data = res.json()
    assert "token" in login_data
    token = login_data["token"]
    print("   Login OK, token:", token)

    print("4. Testing Auth: /auth/me with Bearer token")
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    user_info = res.json()
    assert user_info["email"] == test_email
    print("   Auth /me OK:", user_info)

    print("5. Testing Deals: /deals/top")
    res = client.get("/deals/top?limit=2")
    assert res.status_code == 200
    deals_data = res.json()
    assert "deals" in deals_data
    print("   Top deals count:", len(deals_data["deals"]))

    print("6. Testing Wishlist: add, list, delete")
    # Add
    res = client.post(
        "/wishlist/add",
        json={
            "external_id": "test_game_999",
            "title": "Cyberpunk 2077 Test",
            "thumb_url": "https://example.com/thumb.jpg",
            "target_price": 29.99
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in [200, 201]
    add_data = res.json()
    item_id = add_data.get("item_id")
    print("   Wishlist Add OK, item_id:", item_id)

    # List
    res = client.get("/wishlist", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    wishlist = res.json()
    assert isinstance(wishlist, list)
    assert any(item["id"] == item_id for item in wishlist)
    print("   Wishlist List OK, total items:", len(wishlist))

    # Remove
    res = client.delete(f"/wishlist/{item_id}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    print("   Wishlist Delete OK")

    print("\nALL API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_api()
