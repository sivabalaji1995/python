# python

msal

Microsoft Authentication Library for Python.
Used to authenticate your application or user with Azure Active Directory and acquire access tokens for calling Microsoft APIs like Microsoft Graph.
pandas
A powerful data manipulation and analysis library.
Provides data structures like DataFrames for handling tabular data efficiently.
Useful for processing, analyzing, and transforming data within your Python scripts.
requests
A popular Python HTTP library for making HTTP requests simple and human-friendly.
Used to send GET, POST, PUT, DELETE requests to REST APIs, including Microsoft Graph.
python-dotenv
Loads environment variables from a .env file into your Python environment.
Helps keep sensitive data like client secrets and configuration out of your source code and manage them securely.

=======================================================================================================================

App registration + permissions (portal steps)

Step-by-Step Explanation for App Registration & Permissions in Azure AD:
1. App Registration
You go to Azure Portal → Microsoft Entra ID (Azure Active Directory) → App registrations → New registration.
Here you create a new application identity that represents your script or service.
After registration, you get:
Application (client) ID: Unique ID of your app.
Directory (tenant) ID: ID of your Azure AD tenant (organization).
These IDs identify your app and the tenant it belongs to.
2. Certificates & Secrets
Under Certificates & secrets, you create a new client secret — basically a password your app uses to authenticate securely.
Important: You must copy this secret now because it’s shown only once.
Your app will use this secret along with the client ID to prove its identity when requesting tokens.
3. API Permissions
Your app needs permissions to access Microsoft Graph API to perform operations like creating users.
In API permissions → Add a permission → Microsoft Graph → Application permissions, you add:
User.ReadWrite.All — allows your app to read and write user profiles (required to create or update users).
Directory.ReadWrite.All — more privileged; allows modifying directory objects like groups (only add if your script needs it).
These are application permissions, meaning your app acts without a signed-in user (non-interactive).
4. Grant Admin Consent
Because these permissions are powerful, an administrator must grant admin consent to approve them for your organization.
Without this, your app won’t be authorized to use these permissions even if requested.
5. Why this is needed for Client Credentials Flow
The client credentials flow is used by apps/scripts running in the background without user interaction.
To create users or perform directory operations, the app must have app-only permissions granted by admin consent.
This way, your script can authenticate itself using client ID and secret and operate securely and autonomously.
6. Best Practice: Use Environment Variables
Store your Tenant ID, Client ID, and Client Secret securely as environment variables (.env file or system environment).
Avoid hardcoding secrets in your code to prevent accidental exposure.

=================================================================================================================================================

AUTHORITY: Where your app authenticates (your tenant’s Azure AD).  
SCOPE: What permissions you want in the token (all assigned Microsoft Graph app permissions).  
GRAPH_ENDPOINT: The specific Microsoft Graph API URL your app calls (here, for user management).

==================================================================================================================================================

```python
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
```

1. **Create a ConfidentialClientApplication object:**  
This initializes an MSAL client representing your confidential application (a backend app or script).  
It uses your app’s client ID and client secret along with the authority URL (your Azure AD tenant endpoint).  
This object handles the communication with Azure AD for authentication.

2. **Acquire an access token for the app:**  
This requests an access token from Azure AD using the client credentials flow.  
It asks for the scopes/permissions specified in `SCOPE` (typically `https://graph.microsoft.com/.default`).  
The result is a dictionary containing either the token or error info.

3. **Check if the token was successfully acquired:**  
If the response contains an `"access_token"`, it returns this token.  
If not, it raises an exception with an error message extracted from the result, indicating why token acquisition failed.

---

**Summary:**  
The function authenticates your app without any user interaction using client credentials.  
It gets a valid OAuth2 access token that your script can use to call Microsoft Graph API.  
If something goes wrong (wrong credentials, no permissions, network issues), it raises a clear error.


==================================================

```python
response = requests.post(GRAPH_ENDPOINT, headers=headers, json=payload)

if response.status_code in (200, 201):
    print(f"✅ Created user: {user_data['displayName']}")
else:
    print(f"❌ Failed to create user: {user_data['displayName']}")
    print(response.status_code, response.text)
```

In the Python `requests` library:

- `requests.post()` is a method used to send an HTTP POST request to a specified URL.  
- It belongs to the `requests` module (not a class called request), and it's a function that simplifies making HTTP POST calls.  
- You provide parameters like:  
  - The URL (here, `GRAPH_ENDPOINT`)  
  - `headers` (for authentication and content type)  
  - `json` (the payload to send in JSON format)  

This method sends the data to the server, which usually means creating or updating a resource (like creating a user in Microsoft Graph API).

---

**In short:**  
- `requests.post()` → Sends a POST HTTP request  
- You give it URL + headers + JSON data  
- It returns a `Response` object containing the server’s reply