import requests
import pandas as pd

api_token = "rFjgPvBWo0XKpzfV5Ogyyb5x0PennjJqPpLjz"  # Replace with your actual token
headers = {"Authorization": f"Bearer {api_token}"}

# 1. Get the workspace ID:
workspace_name = "SVC-PMO PCE (i)"
url = "https://api.smartsheet.com/2.0/workspaces"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    workspaces = response.json()
    for workspace in workspaces['data']:
        if workspace['name'] == workspace_name:
            workspace_id = workspace['id']
            break
    else:
        print(f"Error: Workspace '{workspace_name}' not found.")
        exit(1)
else:
    print(f"Error fetching workspaces: {response.status_code} - {response.text}")
    exit(1)

# 2. Find the sheet ID:
sheet_name = "PCE ALL DETAILS MASTER (A)"
url = f"https://api.smartsheet.com/2.0/sheets"
data = {"includeAll": True, "workspaceId": workspace_id}
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    sheets = response.json()
    for sheet in sheets['data']:
        if sheet['name'] == sheet_name:
            sheet_id = sheet['id']
            break
    else:
        print(f"Error: Sheet '{sheet_name}' not found in workspace.")
        exit(1)
else:
    print(f"Error fetching sheets: {response.status_code} - {response.text}")
    exit(1)

# 3. Get sheet data:
url = f"https://api.smartsheet.com/2.0/sheets/{sheet_id}"
params = {"include": "data"}  # Include cell data in response
response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    sheet_data = response.json()
    
    # Create a DataFrame from sheet data (optional)
    rows = sheet_data['rows']
    columns = [col['title'] for col in sheet_data['columns']]
    data = []
    for row in rows:
        row_data = [cell['displayValue'] for cell in row['cells']]
        data.append(row_data)

    df = pd.DataFrame(data, columns=columns)

    print(df)  # Or further process the DataFrame
else:
    print(f"Error fetching sheet data: {response.status_code} - {response.text}")
