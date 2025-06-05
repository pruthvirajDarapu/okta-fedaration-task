import requests

OKTA_DOMAIN = "https://demo-teal-antlion-29717.okta.com"
API_TOKEN = "00BNjo9Bsn9O-CFS9Xk12DXpdVAhsnYJ1QAOBSlLCa"
OFFICE_365_APP_NAME = "demo-okta-Office-365"  # App label in Okta

headers = {
    "Authorization": f"SSWS {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_app_id(app_name):
    url = f"{OKTA_DOMAIN}/api/v1/apps?q={app_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json():
        return response.json()[0]["id"]
    else:
        print(f"App '{app_name}' not found.")
        return None

def assign_app_to_user(app_id, user_id):
    url = f"{OKTA_DOMAIN}/api/v1/apps/{app_id}/users/{user_id}"
    response = requests.post(url, json={}, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Assigned app to user successfully.")
    else:
        print(f"Failed to assign app: {response.status_code} {response.text}")

def create_user(first_name, last_name, login, email, password):
    url = f"{OKTA_DOMAIN}/api/v1/users?activate=true"
    payload = {
        "profile": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "login": login
        },
        "credentials": {
            "password": {"value": password}
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"User {login} created successfully.")
        user_id = response.json()["id"]

        # Optional: Send reset password email
        reset_url = f"{OKTA_DOMAIN}/api/v1/users/{user_id}/lifecycle/reset_password?sendEmail=true"
        reset_response = requests.post(reset_url, headers=headers)
        if reset_response.status_code == 200:
            print(f"Password reset email sent to {email}.")
        else:
            print(f"Failed to trigger password reset: {reset_response.status_code} {reset_response.text}")

        # ✅ Assign Office 365 app to user
        app_id = get_app_id(OFFICE_365_APP_NAME)
        if app_id:
            assign_app_to_user(app_id, user_id)

    else:
        print(f"Failed to create user: {response.status_code} {response.text}")


# Example usage:
create_user("New", "User", "new.user@a114.mywiclab.com", "new.user@a114.mywiclab.com", "P@ssword1234")
