import os
import json
import requests

def strTolist(str):
    res=str.strip('[')
    res=res.strip(']')
    res=res.split(',')
    return res

def download_proxies(subscribe_url,save_filename):
     # 目标 URL
    url = subscribe_url

    # 自定义 User-Agent
    headers = {
        "User-Agent": "clashmeta"
    }

    # 发送 GET 请求
    response = requests.get(url, headers=headers)

    # 检查响应是否成功
    if response.status_code == 200:
        # 保存文件
        with open(save_filename, "wb") as file:
            file.write(response.content)
        print("文件已成功下载并保存为 "+save_filename)
    else:
        print(f"下载失败，状态码: {response.status_code}")
    
if __name__ == "__main__":

    subs=os.environ.get("PROXIES")
    subs=strTolist(subs)
    i=0
    for subs_url in subs:
        i+=1
        download_proxies(subs_url,f"proxy_{i}.yaml")
        
   
