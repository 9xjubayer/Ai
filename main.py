import requests
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

API_KEY = "AIzaSyBQYlyKeTpOiCoCvlCP0v8WIw_im9RqA38"
VALID_KEY = "JUBAYER"

def try_gemini(question):
    # যে যে এড্রেসগুলো কাজ করতে পারে তার লিস্ট
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    ]
    
    payload = {"contents": [{"parts": [{"text": question}]}]}
    
    for url in endpoints:
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            if "candidates" in result:
                return result['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
    return None

@app.get("/")
def home():
    return {"status": "Online", "msg": "Use /ask?key=JUBAYER&question=hi"}

@app.get("/ask")
async def ask_ai(key: str = Query(...), question: str = Query(...)):
    if key != VALID_KEY:
        raise HTTPException(status_code=403, detail="Invalid Key")

    answer = try_gemini(question)
    
    if answer:
        return {"status": "success", "answer": answer}
    else:
        return {
            "status": "error", 
            "message": "Google API is rejecting all models. Please check if your API Key is active in Google AI Studio."
        }
