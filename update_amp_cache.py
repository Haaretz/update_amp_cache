# import OpenSSL
from OpenSSL import crypto
import base64
import time
import re
import os,sys
import requests

update_cache_url="https://cdn.ampproject.org/caches.json"
privatekey_path = os.getenv("PRIVATE_KEY","private-key.pem")
privatekey = open(privatekey_path).read()


def keySign(data,private_key=privatekey):    
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)
    sign = crypto.sign(pkey, data.encode(), "sha256") 
    return base64.b64encode(sign).decode('UTF8').replace("/","_").replace("+","-").rstrip("=")

def get_flush_url(updateCacheApiDomainSuffix,url):
    url = re.sub("^https?://","",url)
    url = re.sub("[\?,#,&].+","",url)
    domain = url.split("/",1)[0].replace(".","-")
    amp_ts = int(time.time())
    si_url = "/update-cache/c/s/{}?amp_action=flush&amp_ts={}".format(url,amp_ts)
    amp_url_signature = keySign(si_url)        
    return "https://{}.{}{}&amp_url_signature={}".format(domain,updateCacheApiDomainSuffix,si_url,amp_url_signature)


def get_updateCacheApiDomainSuffix(url=update_cache_url):
    r = requests.get(url)
    updateCacheApiDomainSuffix = {}
    if r.status_code != 200:
        sys.exit("ERROR: unable to get updateCacheApiDomainSuffix from utl: " + url)
    resp = r.json()
    for apiDomain in resp["caches"]:
        updateCacheApiDomainSuffix[apiDomain["id"]] = apiDomain["updateCacheApiDomainSuffix"]
    return updateCacheApiDomainSuffix     
    
    
def updateCache(url):
    global update_cache_url
    updateCacheApiDomainSuffix = get_updateCacheApiDomainSuffix(update_cache_url)
    for k,v in updateCacheApiDomainSuffix.items():
        if k == "bing":
            continue
        update_cache_url = get_flush_url(v,url)
        r = requests.get(update_cache_url)
        if r.status_code != 200:
            print("Error: status code {} when purging cache on {} \n\turl: {}\n\t{}".format(r.status_code,k ,update_cache_url,r.txt))
        else:
            print("Update cache Success on {}!\n\t{}".format(k,url))    

