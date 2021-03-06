import json
from flask import Flask, request
import update_amp_cache
app = Flask(__name__)

updateCacheApiDomains = update_amp_cache.get_updateCacheApiDomainSuffix(update_amp_cache.update_cache_url)




@app.route("/update-cache", methods=["POST"])
def update_cache():        
        req = request.get_json()
        if req.__class__ != dict:
            return {"status": "error","message":"perhaps missing Content-Type: application/json"}, 500
        if "url" in req:
            url = req["url"]            
            update_amp_cache.updateCache(url,updateCacheApiDomains)
            return {"status":"success","message":"url cache updated" }, 200
        else:
            return {"status":"error","message":"payload not containing any url" }, 500
        





if __name__ == '__main__':
    app.run(host="0.0.0.0")
