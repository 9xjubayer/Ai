import os
import requests
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

# আপনার আসল API Key এবং মডেল কনফিগারেশন
API_KEY = "AIzaSyD9mZ6fK-jaPyGIPIFhU35cI0-m0HaemBE"
VALID_KEY = "JUBAYER"

@app.get("/")
def home():
    return {"status": "API is online", "endpoint": "/ask"}

@app.get("/ask")
async def ask_ai(key: str = Query(...), question: str = Query(...)):
    # সিকিউরিটি চেক
    if key != VALID_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # সরাসরি Google API URL (এখানেই আসল জাদু)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": question}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # উত্তরটি বের করে আনা
        if "candidates" in result:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return {
                "status": "success",
                "answer": answer
            }
        else:
            return {"status": "error", "message": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}
