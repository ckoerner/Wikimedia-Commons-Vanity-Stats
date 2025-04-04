import http.client
import json
import urllib.parse
import csv
import sys
import os
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Customizable Parameters ===
commons_host = "commons.wikimedia.org"
analytics_host = "wikimedia.org"
commons_path = "/w/api.php"
analytics_path = "/api/rest_v1/metrics/mediarequests/per-file/all-referers/user"

# User settings
username = input("Enter username (default: Ckoerner): ") or "Ckoerner"

# Fetch account creation date
user_info_params = {
    "action": "query",
    "list": "users",
    "ususers": username,
    "usprop": "registration",
    "format": "json"
}
user_data = http.client.HTTPSConnection(commons_host)
user_data.request("GET", commons_path + "?" + urllib.parse.urlencode(user_info_params), headers={"Accept": "application/json"})
response = user_data.getresponse()
user_info = json.loads(response.read().decode())
user_data.close()

registration_date = "20130122"  # Default fallback
if "query" in user_info and "users" in user_info["query"] and "registration" in user_info["query"]["users"][0]:
    registration_date = user_info["query"]["users"][0]["registration"].replace("-", "")[0:8]

# Set default end_date to current date
current_date = datetime.datetime.now().strftime("%Y%m%d")

analytics_frequency = input("Enter analytics frequency (daily/monthly, default: daily): ") or "daily"
start_date = input(f"Enter start date (YYYYMMDD, default: {registration_date}): ") or registration_date
end_date = input(f"Enter end date (YYYYMMDD, default: {current_date}): ") or current_date
output_csv = input("Enter output CSV filename (default: media_requests.csv): ") or "media_requests.csv"
max_files_to_check = int(input("Enter max files to check (default: 500): ") or 500)
num_threads = int(input("Enter number of parallel threads (default: 5): ") or 5)

# Function to make API requests
def make_request(host, path, params=None):
    conn = http.client.HTTPSConnection(host)
    if params:
        path += "?" + urllib.parse.urlencode(params)
    conn.request("GET", path, headers={"Accept": "application/json"})
    response = conn.getresponse()
    data = response.read().decode()
    conn.close()
    return json.loads(data) if data else {}

# Function to get the correct file path from the MediaWiki API
def get_file_path(title):
    file_info_params = {
        "action": "query",
        "titles": f"File:{title}",
        "prop": "imageinfo",
        "iiprop": "url|timestamp",
        "format": "json"
    }
    data = make_request(commons_host, commons_path, file_info_params)
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "imageinfo" in page:
            file_info = page["imageinfo"][0]
            return file_info["url"].split("commons/")[-1], file_info.get("timestamp")  # Extract correct file path and upload timestamp
    return None, None

# Function to fetch media request data for a file
def fetch_media_requests(file_title):
    file_path, upload_date = get_file_path(file_title)
    if not file_path:
        return None  # Skip if unable to retrieve file path

    encoded_title = urllib.parse.quote(f"/wikipedia/commons/{file_path}", safe='')
    analytics_endpoint = f"{analytics_path}/{encoded_title}/{analytics_frequency}/{start_date}/{end_date}"
    analytics_data = make_request(analytics_host, analytics_endpoint)

    if 'status' in analytics_data and analytics_data['status'] == 404:
        return None  # Skip files with no data found
    elif 'items' in analytics_data:
        requests_count = sum(item.get('requests', 0) for item in analytics_data['items'])
        if requests_count > 0:
            return (file_title, requests_count, upload_date)
    return None

# Fetch list of uploaded files with pagination
files = []
params = {
    "action": "query",
    "list": "allimages",
    "aiuser": username,
    "aisort": "timestamp",
    "aidir": "ascending",
    "ailimit": "500",
    "format": "json"
}
while True:
    data = make_request(commons_host, commons_path, params)
    batch_files = data.get("query", {}).get("allimages", [])
    files.extend(batch_files)
    
    if "continue" in data:
        params["aicontinue"] = data["continue"]["aicontinue"]
    else:
        break
    
    if len(files) >= max_files_to_check:
        files = files[:max_files_to_check]
        break

# Counter for files checked
files_checked = 0
results = []

# Open a CSV file to store the results
with open(output_csv, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["File Name", f"Media Requests ({analytics_frequency.capitalize()})", "Upload Date"])  # Header row

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_file = {executor.submit(fetch_media_requests, file['title'].replace("File:", "")): file for file in files}
        for future in as_completed(future_to_file):
            files_checked += 1
            print(f"Files checked: {files_checked}", end='\r', flush=True)  # Update counter in-place
            result = future.result()
            if result:
                csv_writer.writerow(result)  # Write to CSV
                print(f"{result[0]}: {result[1]} media requests ({analytics_frequency})")

# Print the final count of files checked
csv_full_path = os.path.abspath(output_csv)
print(f"\nTotal files checked: {files_checked}")
print(f"Results saved to {csv_full_path}")
