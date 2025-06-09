import subprocess
import requests

OKTA_DOMAIN = "https://demo-teal-antlion-29717-admin.okta.com"
API_TOKEN = "00BNjo9Bsn9O-CFS9Xk12DXpdVAhsnYJ1QAOBSlLCa"

def delete_user_from_okta(login):
    headers = {
        "Authorization": f"SSWS {API_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"{OKTA_DOMAIN}/api/v1/users/{login}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_id = response.json()["id"]
        print(f"Found user {login} with ID: {user_id}")

        deactivate_url = f"{OKTA_DOMAIN}/api/v1/users/{user_id}/lifecycle/deactivate"
        deactivate_response = requests.post(deactivate_url, headers=headers)

        if deactivate_response.status_code == 200:
            print(f"User {login} deactivated successfully.")

            delete_url = f"{OKTA_DOMAIN}/api/v1/users/{user_id}"
            delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 204:
                print(f"User {login} deleted from Okta.")
            else:
                print(f"Failed to delete user from Okta: {delete_response.status_code} {delete_response.text}")
        else:
            print(f"Failed to deactivate user: {deactivate_response.status_code} {deactivate_response.text}")
    else:
        print(f"User {login} not found in Okta: {response.status_code} {response.text}")

def delete_user_from_azure_ad(user_principal_name):
    powershell_command = f'''
Import-Module Microsoft.Graph.Users
Connect-MgGraph -Scopes "User.ReadWrite.All"
Remove-MgUser -UserId "{user_principal_name}" -Confirm:$false
'''
    try:
        subprocess.run(["powershell", "-Command", powershell_command], check=True)
        print(f"User {user_principal_name} deleted from Azure AD (Microsoft Graph).")
    except subprocess.CalledProcessError as e:
        print(f"Failed to delete user from Azure AD: {e}")

# Example usage:
# List of users to delete
users_to_delete = [
    "elon.musk@a114.mywiclab.com"
]

for user_login in users_to_delete:
    delete_user_from_okta(user_login)
    delete_user_from_azure_ad(user_login)

