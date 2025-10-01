import requests
import sys
import urllib3


# CONFIGURATION
NETBOX_URL = "https://netbox.mfreiremelguizo01.com/api"
API_TOKEN = "1495dae42f4cda16290a12d8a2ddd9a6513e09a8"

HEADERS = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# FUNCTION
def get_sites_by_status(status):
    """Query NetBox API for sites with a specific status."""
    url = f"{NETBOX_URL}/dcim/sites/?status={status}"

    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch sites → {e}")
        return
    except ValueError:
        print("Error: Response is not valid JSON")
        return

    if not results:
        print(f"No sites found with status '{status}'.")
    else:
        print(f"Sites with status '{status}':")
        for site in results:
            print(f"- {site['name']} (Slug: {site['slug']}, ID: {site['id']})")


# MAIN
if __name__ == "__main__":
    if len(sys.argv) > 2 or not sys.argv[1].strip():
        print("Error: incorrect number of arguments.")
        sys.exit(1)

    status = sys.argv[1]
    get_sites_by_status(status)
