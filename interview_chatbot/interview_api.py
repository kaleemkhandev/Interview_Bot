from fastapi import FastAPI, UploadFile, File,Query,Body
from typing import List,Dict
import uvicorn
from utils2 import return_questions
app = FastAPI()

@app.post("/interview_bot")
async def signin(data):

    try:
       model_id = data.id
       model_key = data.model_key
       prompt = data.prompt
       user_id = data.user_id
       job_role = data.job_role
       questions = return_questions(model_id,model_key,prompt,user_id,job_role)
       if type(questions) != list:
           return {"Exception Occured":questions}
       
       response = {"questions":questions}
       return response 
    except Exception as e:
        return e
    
if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=5000)

