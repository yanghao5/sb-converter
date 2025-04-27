import glob
import os
import sys
import yaml
import json
import requests
from cloudflare import Cloudflare

def get_proxy_files():
    return glob.glob(os.path.join(os.getcwd(), "proxy_*.yaml"))

def current_proxies(files):
    currentproxies=[]
    for file in files:
        with open(file, "r") as file:
            data = yaml.safe_load(file)
        proxies = data.get('proxies', [])
        keywords = ['流量', '到期', '重置', '官网', '收藏', '超时']
        filtered_proxies=[proxy for proxy in proxies if not any(keyword in proxy['name'] for keyword in keywords)]
        currentproxies.extend(filtered_proxies)
        
    with open("current_proxies_nodes.json", "w", encoding="utf-8") as json_file:
        json.dump(currentproxies, json_file, ensure_ascii=False, indent=4)
        print("过滤后的 proxies 已保存到 'current_proxies_nodes.json' 文件中")
    # 直接返回 filtered_proxies_nodes 列表，不需要再用 json.loads
    return currentproxies

def get_oldproxies():
    client = Cloudflare(
    api_email=os.environ.get("CLOUDFLARE_EMAIL"),  # This is the default and can be omitted
    api_key=os.environ.get("CLOUDFLARE_API_KEY"),  # This is the default and can be omitted
    )
    value = client.kv.namespaces.values.get(
        key_name="proxies",
        account_id=os.environ.get("CF_ACCOUNT_ID"),
        namespace_id=os.environ.get("KV_NAMESPACE_ID"),
    )
    content = value.read()
    oldproxies = json.loads(content)
    with open("old_proxies_nodes.json", "w", encoding="utf-8") as json_file:
        json.dump(oldproxies, json_file, ensure_ascii=False, indent=4)
    print("已保存到 old_proxies_nodes.json")
    return oldproxies


def upload_proxies(currentproxies):
    email = os.environ.get("CLOUDFLARE_EMAIL")  # Cloudflare account email
    account_id = os.environ.get("CF_ACCOUNT_ID")  # Cloudflare account ID
    namespace_id = os.environ.get("KV_NAMESPACE_ID")  # Cloudflare KV namespace ID
    api_key = os.environ.get("CLOUDFLARE_API_KEY")  # Cloudflare API key

    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk'

    data = [
        {
            "key": "proxies",
            "value": json.dumps(currentproxies)
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

def compare_proxies(current, old):    
    if current == old:
        print("The JSON objects are equal.")
    else:
        print("The JSON objects are different.")
        print("Upload current proxies")
        upload_proxies(current)
        print(type(current))
        sys.stderr.write("Error: The JSON objects are different.\n")

if __name__ == "__main__":
    files=get_proxy_files()
    currentproxies=current_proxies(files)
    oldproxies=get_oldproxies()
    compare_proxies(currentproxies,oldproxies)
