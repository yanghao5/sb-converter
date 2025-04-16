import os
import json
import requests

# cfkv
# upload proxies

# pip install requests
email = os.environ.get("CLOUDFLARE_EMAIL")  # Cloudflare account email
account_id = os.environ.get("CF_ACCOUNT_ID")  # Cloudflare account ID
namespace_id = os.environ.get("KV_NAMESPACE_ID")  # Cloudflare KV namespace ID
api_key = os.environ.get("CLOUDFLARE_API_KEY")  # Cloudflare API key

with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)  

json_str = json.dumps(data, ensure_ascii=False)  

url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk'

data = [
    {
        "key": "sb",
        "value": json_str
    }
]

headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': email,
    'X-Auth-Key': api_key
}

response = requests.put(url, headers=headers, json=data)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
