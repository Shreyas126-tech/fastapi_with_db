
import requests
import json
import random
import string

BASE_URL = "http://127.0.0.1:8000"

def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def test_signup_and_login():
    # Generate random user data
    name = generate_random_string()
    email = f"{name}@example.com"
    password = "securepassword123"

    print(f"Testing with User: {name}, Email: {email}, Password: {password}")

    # 1. Signup
    signup_data = {
        "name": name,
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/signup", json=signup_data)
    print(f"Signup Response Status: {response.status_code}")
    print(f"Signup Response Body: {response.json()}")
    
    if response.status_code != 200:
        print("Signup failed!")
        return

    # 2. Login (Success)
    login_data = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login (Success) Response Status: {response.status_code}")
    if response.status_code == 200:
        print("Login successful!")
        token = response.json()
        print(f"Token received: {token.get('access_token')[:20]}...")
    else:
        print(f"Login failed! Body: {response.json()}")

    # 3. Login (Failure - Wrong Password)
    wrong_login_data = {
        "email": email,
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=wrong_login_data)
    print(f"Login (Failure) Response Status: {response.status_code}")
    if response.status_code == 401:
        print("Login failed as expected (Password mismatch).")
    else:
        print(f"Unexpected response for wrong password: {response.status_code}")

if __name__ == "__main__":
    try:
        test_signup_and_login()
    except Exception as e:
        print(f"An error occurred: {e}")
