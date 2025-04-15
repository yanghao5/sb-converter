import json
import os 

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

    subs=os.environ.get("PROXIES")
    subs=strTolist(subs)
    createProviders(subs)
