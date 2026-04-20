# Azure Utilities Repository

A collection of Python utilities for managing Azure resources, including VM lifecycle management and bulk user creation in Azure AD.

---

## Overview

This repository contains two main modules:

1. **stopvms** — Stop / deallocate Azure Virtual Machines tagged with `env=dev` in a specified resource group.
2. **usercreation** — Create users in bulk in Azure AD via Microsoft Graph API using client credentials flow.

All code uses Azure Python SDKs and requires appropriate Azure credentials and permissions to run.

---

## Repository Structure

```
.
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── stopvms/
│   ├── README.md                       # Notes on Azure credential and compute client usage
│   ├── stopvm.py                       # Sample script: list and deallocate VMs by tag
│   └── deallocatevm.py                 # Helper script: deallocate VMs and display power states
└── usercreation/
    ├── README.md                       # Notes on MSAL, app registration, and token flow
    ├── usercreation.py                 # Main script: read CSV and create users via MS Graph
    └── users.csv                       # Input CSV with user data for bulk creation
```

---

## Module Details

### stopvms

**Purpose:** Stop Azure Virtual Machines tagged as development (`env=dev`) to reduce compute costs.

**Files:**
- **stopvm.py**: Iterates over VMs in a resource group, identifies those with `env=dev` tag, and deallocates them using `ComputeManagementClient.begin_deallocate()`.
- **deallocatevm.py**: Provides a reusable function `deallocate_vm(rgname)` that handles the same operation and prints power state details (e.g., `"VM deallocated"`) by querying `instance_view.statuses`.

**Key Components:**
- `DefaultAzureCredential` — Auto-discovers credentials (env vars, Managed Identity, Azure CLI login, VS Code credentials, etc.).
- `ComputeManagementClient` — Azure SDK client for VM management operations.

**Usage:**
```bash
python3 stopvms/deallocatevm.py
# Enter resource group name when prompted
```

**Requirements:**
- Azure subscription ID (hardcoded or via env var).
- Local authentication (e.g., `az login` or environment credentials).
- Run-time access to the target resource group.

---

### usercreation

**Purpose:** Bulk-create users in Azure AD by reading a CSV file and posting to Microsoft Graph API.

**Files:**
- **usercreation.py**: Reads `users.csv`, acquires an access token via MSAL client credentials flow, and calls MS Graph `POST /users` endpoint for each row.
- **README.md**: Documents the app registration process, permissions (User.ReadWrite.All), and token acquisition flow.

**Key Components:**
- `msal.ConfidentialClientApplication` — Handles OAuth2 client credentials flow.
- `requests.post()` — Makes HTTP POST requests to Microsoft Graph.
- `pandas.read_csv()` — Parses the input CSV file.

**CSV Format:**
The `users.csv` file must include at least these columns (case-sensitive as used in the code):
- `displayName` — User's display name.
- `mailNickname` — User's mail nickname (alias).
- `userPrincipalName` — User's UPN (e.g., `user@tenant.onmicrosoft.com`).
- `password` — Initial password (user will be forced to change on first sign-in).

**Usage:**
```bash
python3 usercreation/usercreation.py
```

**Requirements:**
- Azure AD app registration with credentials (Tenant ID, Client ID, Client Secret).
- App permissions: `User.ReadWrite.All` (Application permissions, admin consent required).
- `users.csv` file in the working directory.

---

## Dependencies

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Core packages:**
- **azure-identity** — Azure credential management (`DefaultAzureCredential`).
- **azure-mgmt-compute** — Azure VM management client.
- **msal** — Microsoft Authentication Library for OAuth2 client credentials.
- **pandas** — CSV reading and data manipulation.
- **requests** — HTTP library for Microsoft Graph API calls.
- **python-dotenv** — (Recommended) Load environment variables from `.env` file.

---

## Configuration & Environment Setup

### For stopvms:
1. Set your Azure subscription ID (currently hardcoded; move to `AZURE_SUBSCRIPTION_ID` env var).
2. Authenticate locally:
   ```bash
   az login
   ```
   Or set environment variables for service principal authentication:
   ```bash
   export AZURE_CLIENT_ID="your-client-id"
   export AZURE_CLIENT_SECRET="your-client-secret"
   export AZURE_TENANT_ID="your-tenant-id"
   ```

### For usercreation:
1. Create an Azure AD app registration:
   - Go to **Azure Portal** → **Microsoft Entra ID** → **App registrations** → **New registration**.
   - Record the **Application (client) ID** and **Directory (tenant) ID**.
   - Under **Certificates & secrets**, create a new **client secret** and copy it immediately.
   - Under **API permissions**, add Microsoft Graph **Application** permission: `User.ReadWrite.All`.
   - Request admin consent.

2. Set environment variables (or hard-code in `usercreation.py`—not recommended):
   ```bash
   export TENANT_ID="your-tenant-id"
   export CLIENT_ID="your-client-id"
   export CLIENT_SECRET="your-client-secret"
   ```

3. Prepare `users.csv` with required fields.

---

## Security Recommendations

⚠️ **Critical:** The current `usercreation/usercreation.py` contains hard-coded credentials (Tenant ID, Client ID, Client Secret). This is a security risk.

**Recommended Actions:**
1. **Remove all hard-coded secrets** from source code immediately.
2. **Use environment variables** or a secret management service:
   ```python
   import os
   TENANT_ID = os.environ.get("TENANT_ID")
   CLIENT_ID = os.environ.get("CLIENT_ID")
   CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
   ```
3. **Add `.env` to `.gitignore`** and use `python-dotenv` for local development:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
4. **Create `.env.example`** with placeholder values for documentation.
5. **Never print tokens or secrets** to logs or console output.
6. **Implement error handling** to avoid leaking sensitive information in error messages.

---

## Running the Scripts

### Stop VMs:
```bash
cd /Users/sivabalaji/Sivas_folder/git_repo/python
python3 stopvms/deallocatevm.py
# When prompted: enter resource group name
```

### Create Users:
```bash
cd /Users/sivabalaji/Sivas_folder/git_repo/python
python3 usercreation/usercreation.py
# Ensure users.csv is in the working directory
# Example output:
#   ✅ Created user: John Doe
#   ✅ Created user: Jane Smith
```

---

## Notes & Observations

- **Async operations:** VM deallocation (`begin_deallocate`) is asynchronous. Some scripts call `.result()` to wait for completion; others do not. This can affect status reporting.
- **Tag handling:** `stopvm.py` accesses `vm.tags['env']` directly (will crash if tag missing), while `deallocatevm.py` uses safer `.get()` method. The latter is more robust.
- **CSV dependency:** The user creation script assumes `users.csv` exists in the current working directory. Consider adding error handling for missing files.
- **Graph API versioning:** The script uses the stable MS Graph endpoint (`v1.0`). Newer beta features are available but may change.

---

## Suggested Improvements

1. Move hard-coded credentials to environment variables.
2. Populate `requirements.txt` with pinned versions (e.g., `azure-identity==1.14.0`).
3. Add `.env.example` as a template.
4. Improve error handling and logging across both modules.
5. Add unit tests or integration tests.
6. Consider adding a `--dry-run` flag to preview operations before executing.
7. Add CLI argument parsing (e.g., `argparse`) for flexible resource group and user file inputs instead of interactive prompts.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DefaultAzureCredential` fails to authenticate | Ensure `az login` is run or env vars are set. Check `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`. |
| User creation returns 403 Forbidden | Verify app registration permissions are set to `User.ReadWrite.All` and admin consent was granted. |
| CSV file not found | Ensure `users.csv` is in the same directory as the script or update file path in code. |
| `KeyError: 'env'` in stopvm.py | The target VM does not have the `env` tag. Use `deallocatevm.py` (safer) or add error handling. |

---

## References

- [Azure Identity for Python](https://learn.microsoft.com/python/api/azure-identity/)
- [Azure Compute Management Client](https://learn.microsoft.com/python/api/azure-mgmt-compute/)
- [MSAL for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)
- [Microsoft Graph API](https://learn.microsoft.com/graph/)
- [Create User in MS Graph](https://learn.microsoft.com/graph/api/user-post-users)
