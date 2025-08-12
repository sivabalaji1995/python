import pandas as pd
import msal
import requests


TENANT_ID = "a0977b0c-428a-4396-9992-d35626fb0508"
CLIENT_ID = "82e2dfe4-6b52-4b91-9531-b0a1776d139e"
CLIENT_SECRET = "QHf8Q~gDiVcoMdOMkP5L-sRZ-yxaBP1a994Dub8q"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]  
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/users"

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
        raise Exception("Could not obtain access token: " + str(result.get("error_description", "Unknown error")))
    

def create_user(access_token, user_data):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "accountEnabled": True,
        "displayName": user_data["displayName"],
        "mailNickname": user_data["mailNickname"],  
        "userPrincipalName": user_data["userPrincipalName"],
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": user_data["password"]
        }
    }

    response = requests.post(GRAPH_ENDPOINT, headers=headers, json=payload)

    if response.status_code in (200, 201):
        print(f"✅ Created user: {user_data['displayName']}")
    else:
        print(f"❌ Failed to create user: {user_data['displayName']}")
        print(response.status_code, response.text)


if __name__ == "__main__":

    token = get_access_token()

    df = pd.read_csv("users.csv")

    for _, row in df.iterrows():
         create_user(token, row)
