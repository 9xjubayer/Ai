import os
from fastapi import FastAPI, HTTPException, Query
import google.generativeai as genai

app = FastAPI()

# আপনার API Key
API_KEY = "AIzaSyD9mZ6fK-jaPyGIPIFhU35cI0-m0HaemBE"
genai.configure(api_key=API_KEY)

# ফিক্সড মডেল কনফিগারেশন
model = genai.GenerativeModel("gemini-1.5-flash")

VALID_KEY = "JUBAYER"

@app.get("/")
def home():
    return {"message": "API is Live!", "usage": "/ask?key=JUBAYER&question=Hello"}

@app.get("/ask")
async def ask_ai(key: str = Query(...), question: str = Query(...)):
    if key != VALID_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    try:
        # সরাসরি কন্টেন্ট জেনারেট করা
        response = model.generate_content(question)
        
        # টেক্সট ফিল্টার করা
        if response and response.text:
            return {
                "status": "success",
                "answer": response.text
            }
        else:
            return {"status": "error", "message": "Empty response from AI"}
            
    except Exception as e:
        # এরর মেসেজ ক্লিন করে দেখানো
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
