import requests
import subprocess
import base64
import uuid

OKTA_DOMAIN = "https://demo-teal-antlion-29717-admin.okta.com"
API_TOKEN = "00BNjo9Bsn9O-CFS9Xk12DXpdVAhsnYJ1QAOBSlLCa"
OFFICE_365_APP_NAME = "demo-okta-Office-365"

def get_app_id(app_label):
    url = f"{OKTA_DOMAIN}/api/v1/apps?q={app_label}&limit=1"
    headers = {
        "Authorization": f"SSWS {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        apps = response.json()
        if apps:
            return apps[0]["id"]
    print(f"Failed to retrieve app ID: {response.status_code} {response.text}")
    return None

def assign_app_to_user(app_id, user_id):
    url = f"{OKTA_DOMAIN}/api/v1/apps/{app_id}/users"
    headers = {
        "Authorization": f"SSWS {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "id": user_id,
        "scope": "USER"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Assigned Office 365 app to user ID: {user_id}")
    else:
        print(f"Failed to assign app: {response.status_code} {response.text}")

def create_and_activate_user(first_name, last_name, login, email, password):
    url = f"{OKTA_DOMAIN}/api/v1/users"
    headers = {
        "Authorization": f"SSWS {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "profile": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "login": login
        },
        "credentials": {
            "password": {
                "value": password
            }
        }
    }
    response = requests.post(f"{url}?activate=false", json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to create user: {response.status_code} {response.text}")
        return None
    user_id = response.json()["id"]
    print(f"User {login} created successfully (ID: {user_id})")

    app_id = get_app_id(OFFICE_365_APP_NAME)
    if app_id:
        assign_app_to_user(app_id, user_id)

    activate_url = f"{OKTA_DOMAIN}/api/v1/users/{user_id}/lifecycle/activate?sendEmail=false"
    activate_response = requests.post(activate_url, headers=headers)
    if activate_response.status_code == 200:
        print(f"User {login} activated successfully.")
    else:
        print(f"Failed to activate user: {activate_response.status_code} {activate_response.text}")

    return user_id

# List of users to be created
users_to_create = [
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "login": "alice.smith@a114.mywiclab.com",
        "email": "alice.smith@a114.mywiclab.com",
        "password": "P@ssword1234"
    },
    {
        "first_name": "Bob",
        "last_name": "Jones",
        "login": "bob.jones@a114.mywiclab.com",
        "email": "bob.jones@a114.mywiclab.com",
        "password": "P@ssword1234"
    },
    # Add more users here
]

for user in users_to_create:
    create_and_activate_user(
        first_name=user["first_name"],
        last_name=user["last_name"],
        login=user["login"],
        email=user["email"],
        password=user["password"]
    )

# Generate ImmutableId
immutable_id = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
print(f"Generated ImmutableId: {immutable_id}")

# Call PowerShell to create Azure AD user
powershell_script = f'''
Connect-AzureAD
New-AzureADUser -DisplayName "{first_name} {last_name}" `
    -UserPrincipalName "{login}" `
    -MailNickname "{login.split('@')[0]}" `
    -AccountEnabled $true `
    -PasswordProfile @{{ Password = "{password}"; ForceChangePasswordNextLogin = $true }} `
    -ImmutableId "{immutable_id}"
'''

subprocess.run(["powershell", "-Command", powershell_script], shell=True)
