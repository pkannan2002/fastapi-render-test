from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class TaskRequest(BaseModel):
    input: str

@app.post("/parse-task")
async def parse_task(request: TaskRequest):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Parse this into a task: {request.input}"}],
        model="llama-3.3-70b-versatile",
    )
    task_data = response.choices[0].message.content
    return {"parsed_task": task_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)