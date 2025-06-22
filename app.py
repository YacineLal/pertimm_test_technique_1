import requests
import time

def create_application(token, email, first_name, last_name):
    url = "https://hire-game.pertimm.dev/api/v1.1/job-application-request/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
    except Exception as e:
        print("Network error:", e)
        return None
    if resp.status_code in (200, 201):
        response = resp.json()
        print("Application created")
        return response.get("url")
    else:
        print("Application creation failed:", resp.status_code, resp.text)
        return None

def application_status(token, status_url, max_wait=25):
    headers = {"Authorization": f"Token {token}"}
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            resp = requests.get(status_url, headers=headers, timeout=10)
            if resp.status_code != 200:
                print("Status check failed:", resp.status_code)
                time.sleep(2)
                continue
            data = resp.json()
            print("Status:", data.get("status"))
            if data.get("status") == "COMPLETED":
                print("Status is COMPLETED")
                return data.get("confirmation_url")
        except Exception as e:
            print("Polling error:", e)
        time.sleep(2)
    print("Timeout: Status did not become COMPLETED in time")
    return None

def confirm_application(token, confirmation_url):
    headers = {"Authorization": f"Token {token}"}
    data = {"confirmed": True}
    try:
        resp = requests.patch(confirmation_url, headers=headers, json=data, timeout=10)
    except Exception as e:
        print("Network error during confirmation:", e)
        return None
    if resp.status_code in (200, 201):
        print("Application confirmed")
        print(resp.json())
        return True
    elif resp.status_code == 404:
        print("Confirmation too late (404)")
        return False
    else:
        print("Confirmation failed", resp.status_code, resp.text)
        return False

if __name__ == "__main__":
    token = input("Enter your token: ")
    email = input("Enter your email: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    start_time = time.time()
    status_url = create_application(token, email, first_name, last_name)
    if not status_url:
        exit(1)
    confirmation_url = application_status(token, status_url, max_wait=25)
    if not confirmation_url:
        exit(1)
    if time.time() - start_time > 30:
        print("More than 30 seconds passed, confirmation will fail")
    confirm_application(token, confirmation_url)
