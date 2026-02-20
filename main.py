import os
from fastapi import FastAPI, HTTPException, Query
import google.generativeai as genai

app = FastAPI()

# আপনার API Key
API_KEY = "AIzaSyD9mZ6fK-jaPyGIPIFhU35cI0-m0HaemBE"
genai.configure(api_key=API_KEY)

# এআই মডেল সেটআপ - এখানে model_name প্যারামিটারটি নিশ্চিত করুন
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

VALID_KEY = "JUBAYER"

@app.get("/")
def home():
    return {"message": "API is Live!", "usage": "/ask?key=JUBAYER&question=Hello"}

@app.get("/ask")
async def ask_ai(key: str = Query(...), question: str = Query(...)):
    # সিকিউরিটি চেক
    if key != VALID_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    try:
        # এআই থেকে উত্তর জেনারেট করা
        response = model.generate_content(question)
        
        # যদি উত্তর খালি না থাকে তবে রিটার্ন করা
        if response.text:
            return {
                "status": "success",
                "answer": response.text
            }
        else:
            return {"status": "error", "message": "No response from AI"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

# টার্মাক্সে টেস্ট করার জন্য (Vercel এটা ইগনোর করবে)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
