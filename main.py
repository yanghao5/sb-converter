import argparse
import json

def strTolist(str):
    res=str.strip('[')
    res=res.strip(']')
    res=res.split(',')
    return res

def createProviders(subscribe):
    with open('providers.json', 'r') as file:
        data = json.load(file)
    data["subscribes"][0]["url"] = subscribe[0] 
    data["subscribes"][1]["url"] = subscribe[1]  
    with open("providers.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="订阅地址")

    parser.add_argument('--subscribe', type=str, help='在 github repo setting 中通过环境变量设置订阅地址')

    args = parser.parse_args()
    sub=strTolist(args.subscribe)
    print(sub)
    createProviders(sub)
