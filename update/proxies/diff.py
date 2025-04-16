import glob
import os
import yaml
import json
from cloudflare import Cloudflare

def get_proxy_files():
    return glob.glob(os.path.join(os.getcwd(), "proxy_*.yaml"))

def current_proxies(files):
    current_subs=[]
    for file in files:
        with open(file, "r") as file:
            data = yaml.safe_load(file)
        proxies = data.get('proxies', [])
        keywords = ['流量', '到期', '重置', '官网', '收藏', '超时']
        filtered_proxies=[proxy for proxy in proxies if not any(keyword in proxy['name'] for keyword in keywords)]
        current_subs.extend(filtered_proxies)
        
    with open("filtered_proxies.json", "w", encoding="utf-8") as json_file:
        json.dump(current_subs, json_file, ensure_ascii=False, indent=4)
        print("过滤后的 proxies 已保存到 'filtered_proxies.json' 文件中")
    # 直接返回 filtered_proxies 列表，不需要再用 json.loads
    return current_subs

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
    json_content = json.loads(content)
    with open("old_proxies.json", "w", encoding="utf-8") as json_file:
        json.dump(json_content, json_file, ensure_ascii=False, indent=4)
    print("已保存到 old_proxies.json")
    return json_content

def compare_proxies(current, old):    
    if current == old:
        print("The JSON objects are equal.")
    else:
        print("The JSON objects are different.")
        sys.stderr.write("Error: The JSON objects are different.\n")

if __name__ == "__main__":
    files=get_proxy_files()
    currentproxies=current_proxies(files)
    oldproxies=get_oldproxies()
    compare_proxies(currentproxies,oldproxies)
