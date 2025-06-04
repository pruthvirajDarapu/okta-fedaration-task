import msal
import requests
import base64
import uuid

# === CONFIGURATION ===
CLIENT_ID = "ca88d5a8-1b7b-4d6e-99a0-0b2d1bf6e05a"
TENANT_ID = "2b77ce0a-6f13-450b-85a5-0ac0aa2fd552"
CLIENT_SECRET = "n1v8Q~i1wNXCmDJ2wWehDgCSkNNB_MZWSD4YRaID"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# === AUTHENTICATION ===
def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Token error: {result.get('error_description')}")

# === CREATE FEDERATED USER ===
def create_federated_user(token, display_name, user_principal_name, password):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Generate a base64-encoded GUID as the immutableId (SourceAnchor)
    immutable_id = base64.b64encode(uuid.uuid4().bytes).decode("utf-8")

    user_data = {
        "accountEnabled": True,
        "displayName": display_name,
        "mailNickname": user_principal_name.split("@")[0],
        "userPrincipalName": user_principal_name,
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": password
        },
        "immutableId": immutable_id
    }

    response = requests.post(f"{GRAPH_API_ENDPOINT}/users", headers=headers, json=user_data)
    if response.status_code == 201:
        print(f"✅ User '{user_principal_name}' created successfully.")
    else:
        print(f"❌ Failed to create user: {response.status_code} - {response.text}")

# === MAIN ===
if __name__ == "__main__":
    try:
        token = get_access_token()
        create_federated_user(token, "Federated User Demo", "federateduser@a114.mywiclab.com", "P@ssword1234")
    except Exception as e:
        print(f"Error: {e}")
