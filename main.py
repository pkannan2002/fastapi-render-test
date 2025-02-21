from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel
import os
import aiocron

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

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI on Render!"}


# Ping the app every 10 minutes to prevent spin-down
@aiocron.crontab("*/10 * * * *")  # Run every 10 minutes
async def ping_self():
    import requests
    requests.get("https://fastapi-ai-test.onrender.com/")

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
