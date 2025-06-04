import msal
import requests

# Config
CLIENT_ID = '5ef7058c-a5fc-4ec0-9e2c-e1a5d9b3d0d2'
CLIENT_SECRET = 'ZMl8Q~5ekf3TgFz6cR4TuChCwR9aL2xEmLEZkcyO'
TENANT_ID = '2b77ce0a-6f13-450b-85a5-0ac0aa2fd552'
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Authenticate and get token
def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result['access_token']
    else:
        raise Exception(f"Could not get access token: {result.get('error_description')}")

# Create a new user
def create_user(token, display_name, user_principal_name, password):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    user_data = {
        "accountEnabled": True,
        "displayName": display_name,
        "mailNickname": user_principal_name.split("@")[0],
        "userPrincipalName": user_principal_name,
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": password
        }
    }
    response = requests.post(f"{GRAPH_API_ENDPOINT}/users", headers=headers, json=user_data)
    if response.status_code == 201:
        print(f"User {user_principal_name} created successfully.")
    else:
        print(f"Failed to create user: {response.status_code} - {response.text}")

# Delete a user by userPrincipalName
def delete_user(token, user_principal_name):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Get user ID first
    response = requests.get(f"{GRAPH_API_ENDPOINT}/users/{user_principal_name}", headers=headers)
    if response.status_code == 200:
        user_id = response.json()["id"]
        del_response = requests.delete(f"{GRAPH_API_ENDPOINT}/users/{user_id}", headers=headers)
        if del_response.status_code == 204:
            print(f"User {user_principal_name} deleted successfully.")
        else:
            print(f"Failed to delete user: {del_response.status_code} - {del_response.text}")
    else:
        print(f"User {user_principal_name} not found.")

if __name__ == "__main__":
    token = get_access_token()

    # Demo: Create a user
    create_user(token, "New User Demo", "newuserdemo@a114.mywiclab.com", "P@ssword1234")

    # Demo: Delete a user
    # delete_user(token, "newuserdemo@a114.mywiclab.com")
