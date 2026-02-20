from fastapi import FastAPI, HTTPException, Query
import google.generativeai as genai
import uvicorn
import os

app = FastAPI()

# আপনার Gemini API Key এখানে দিন
API_KEY = "AIzaSyD9mZ6fK-jaPyGIPIFhU35cI0-m0HaemBE" 
genai.configure(api_key=API_KEY)

# এআই মডেল সেটআপ
model = genai.GenerativeModel('gemini-1.5-flash')

# সিকিউরিটি কী
VALID_KEY = "JUBAYER"

@app.get("/")
def home():
    return {"message": "AI Chat API is Running!", "usage": "/ask?key=JUBAYER&question=Your Question"}

@app.get("/ask")
async def ask_ai(key: str = Query(...), question: str = Query(...)):
    # সিকিউরিটি চেক
    if key != VALID_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    try:
        # এআই থেকে উত্তর নেওয়া
        response = model.generate_content(question)
        return {
            "status": "success",
            "question": question,
            "answer": response.text
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# টার্মাক্সে রান করার জন্য
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
