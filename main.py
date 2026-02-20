import os
from fastapi import FastAPI, HTTPException, Query
import google.generativeai as genai

app = FastAPI()

# আপনার API Key
API_KEY = "AIzaSyD9mZ6fK-jaPyGIPIFhU35cI0-m0HaemBE"
genai.configure(api_key=API_KEY)

# সব মডেলের জন্য একটি লিস্ট ট্রাই করার ফাংশন
def get_model():
    # প্রথমে Gemini 1.5 Flash ট্রাই করবে, না হলে 1.0 Pro
    available_models = ["gemini-1.5-flash", "gemini-pro"]
    for m in available_models:
        try:
            model = genai.GenerativeModel(m)
            # মডেলটি কাজ করছে কি না ছোট টেস্ট
            return model
        except:
            continue
    return None

model = get_model()
VALID_KEY = "JUBAYER"

@app.get("/")
def home():
    return {"status": "running", "model": "gemini-1.5-flash"}

@app.get("/ask")
async def ask_ai(key: str = Query(...), question: str = Query(...)):
    if key != VALID_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    if not model:
        return {"status": "error", "message": "No supported AI models found."}

    try:
        # জেনারেট কন্টেন্ট কল করা
        response = model.generate_content(question)
        
        if response and response.text:
            return {
                "status": "success",
                "answer": response.text
            }
        else:
            return {"status": "error", "message": "AI returned empty response."}
            
    except Exception as e:
        # এরর মেসেজ ক্লিন করে দেখানো
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
