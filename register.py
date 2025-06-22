import requests
import getpass

def register_user(email, password):
    register_url = "https://hire-game.pertimm.dev/api/v1.1/auth/register/"
    data = {
        "email": email,
        "password1": password,
        "password2": password
    }
    try:
        resp = requests.post(register_url, json=data, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Network error during registration:", e)
        return None

    if resp.status_code == 201:
        print("Registration successful!")
        response = resp.json()
        for k in ("uid", "email", "url", "token", "first_name", "last_name", "level"):
            if k in response:
                val = response[k]
                if k == "token" and val:
                    print(f"{k}: {val}")
        return response

    elif resp.status_code == 400:
        try:
            errors = resp.json()
        except Exception:
            print("Registration failed (invalid JSON response).")
            return None
        print("Registration failed (400 Bad Request):")
        for key, value in errors.items():
            print(f"{key}: {value}")
        return None

    elif resp.status_code == 403:
        print("Forbidden: You might not have the right to register or you sent a forbidden field.")
        print(resp.text)
        return None

    elif resp.status_code == 409:
        print("Conflict: User with this email may already exist.")
        print(resp.text)
        return None

    else:
        print(f"Unexpected response code: {resp.status_code}")
        print(resp.text)
        return None

if __name__ == "__main__":
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    register_user(email, password)
