import requests

OKTA_DOMAIN = "https://demo-teal-antlion-29717-admin.okta.com"
API_TOKEN = "00BNjo9Bsn9O-CFS9Xk12DXpdVAhsnYJ1QAOBSlLCa" #00BNjo9Bsn9O-CFS9Xk12DXpdVAhsnYJ1QAOBSlLCa

def delete_user(login):
    headers = {
        "Authorization": f"SSWS {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Step 1: Get user ID by login
    url = f"{OKTA_DOMAIN}/api/v1/users/{login}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_id = response.json()["id"]
        print(f"Found user {login} with ID: {user_id}")

        # Step 2: Deactivate user
        deactivate_url = f"{OKTA_DOMAIN}/api/v1/users/{user_id}/lifecycle/deactivate"
        deactivate_response = requests.post(deactivate_url, headers=headers)

        if deactivate_response.status_code == 200:
            print(f"User {login} deactivated successfully.")

            # Step 3: Delete user
            delete_url = f"{OKTA_DOMAIN}/api/v1/users/{user_id}"
            delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 204:
                print(f"User {login} deleted successfully.")
            else:
                print(f"Failed to delete user: {delete_response.status_code} {delete_response.text}")
        else:
            print(f"Failed to deactivate user: {deactivate_response.status_code} {deactivate_response.text}")
    else:
        print(f"User {login} not found: {response.status_code} {response.text}")

# Example usage:
delete_user("new.user@a114.mywiclab.com")
