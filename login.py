import requests
import getpass

def login_user(email, password):
    login_url = "https://hire-game.pertimm.dev/api/v1.1/auth/login/"
    data = {
        "email": email,
        "password": password
    }
    try:
        resp = requests.post(login_url, json=data, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Network error during login:", e)
        return None

    if resp.status_code == 200:
        response = resp.json()
        token = response.get("token")
        if token:
            print("Login successful! Token acquired:", token)
            return token
        else:
            print("Login response missing token:", response)
            return None
    elif resp.status_code == 401:
        response = resp.json()
        print("Unauthorized (401):", response.get("message", "Unknown error"))
        if "_errors" in response:
            print("Details:", response["_errors"])
        return None
    elif resp.status_code == 400:
        try:
            errors = resp.json()
        except Exception:
            errors = resp.text
        print("Login failed (400 Bad Request):", errors)
        return None
    else:
        print(f"Unexpected login response code: {resp.status_code}")
        print(resp.text)
        return None

if __name__ == "__main__":
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    token = login_user(email, password)
    if token:
        headers = {"Authorization": f"Token {token}"}
        url = "https://hire-game.pertimm.dev/api/v1.1/account/me/"
        resp = requests.get(url, headers=headers)
        print("Account info:", resp.status_code, resp.json())
