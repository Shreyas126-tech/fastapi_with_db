import requests
import json

BASE_URL = "http://localhost:8000"

def test_history_feature():
    # 1. Sign up a test user (ignoring if already exists)
    user_data = {
        "name": "Test User",
        "email": "test_history@example.com",
        "password": "password123"
    }
    requests.post(f"{BASE_URL}/signup", json=user_data)
    
    # 2. Login
    login_data = {
        "email": "test_history@example.com",
        "password": "password123"
    }
    login_res = requests.post(f"{BASE_URL}/login", json=login_data)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Ask AI
    ask_data = {"message": "Hello, this is a test prompt for history."}
    ask_res = requests.post(f"{BASE_URL}/ask", json=ask_data, headers=headers)
    print("Ask AI Response:", ask_res.json())
    
    # 4. Check History
    history_res = requests.get(f"{BASE_URL}/history", headers=headers)
    history = history_res.json()
    print("History:", json.dumps(history, indent=2))
    
    if any(item["prompt"] == "Hello, this is a test prompt for history." for item in history):
        print("SUCCESS: Prompt found in history!")
    else:
        print("FAILURE: Prompt not found in history.")

if __name__ == "__main__":
    test_history_feature()
