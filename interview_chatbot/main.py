from utils2 import create_pdf
import requests
import datetime
from utils2 import pdf_doc_loader
from utils2 import vector_database_creation 
from utils2 import query_database, query_db_gpt3 ,query_db_llama2,load_Llama2


# create the user
name = input("Enter Your name: ")
email = input("Enter your email: ")
created_at = datetime.datetime.now()
formatted_datetime = created_at.strftime("%Y-%m-%d %H:%M:%S")
data = {"name":name,"email":email,"created_at":formatted_datetime,"status":1}

user_save_url = "http://127.0.0.1:8000/users/"
resp_save_user = requests.post(user_save_url, json=data)

if resp_save_user.status_code == 200:
    new_user = resp_save_user.json()
    print("New user created:", new_user)
else:
    print("Failed to create user:", resp_save_user.status_code)



#call api to get the information of newly saved user
user_id = new_user["id"]
get_user_url = f"http://127.0.0.1:8000/users/{user_id}"
resp_get_user = requests.get(get_user_url)
if resp_get_user.status_code == 200:
    new_user = resp_get_user.json()
    print("saved new user is:", new_user)
else:
    print("Failed to get saved user:", resp_get_user.status_code)




# create the interview data point in database
create_interview_url =  "http://127.0.0.1:8000/interviews/"
job_role = input("Enter the job role: ")
user_id_interview_db = user_id
created_at = datetime.datetime.now()
interview_created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
json_interview_db = {"type":job_role,"user_id":user_id_interview_db,"created_at":interview_created_at}
resp_save_interivew = requests.post(create_interview_url,json=json_interview_db)
if resp_save_interivew.status_code == 200:
    new_interview = resp_save_interivew.json()
    print("saved new interview is:", new_interview)
else:
    print("Failed to create interview:", resp_save_interivew.status_code)


print("1. gpt-3.5turbo \n2. gpt-3 FineTuned \n3. Llama-2 FineTuned")
option = input("Select the model no: ")




if option =="1":
    # Collect questions and answers from the user and save them in the end in questions db
    questions_answers = []
    quest_ans =[]
    questions = ["Tell me about yourself?", "What motivated you to apply for this position?",
                "Describe your relevant experience and skill set", "Tell me about a project you're proud of",
                "What are your strengths and weaknesses", "Where do you see yourself in 5 years"]

    for question in questions:
        answer = input(f"{question}: ")
        answered_at = datetime.datetime.now()
        answered_at = answered_at.strftime("%Y-%m-%d %H:%M:%S")
        question_data = {"statement":question,"answer":answer,"interview_id":new_interview["id"],"created_at":answered_at}
        questions_answers.append(question_data)
        quest_ans.append((question,answer))


    # Create a PDF with the collected questions and answers
    pdf_filename = "interview.pdf"
    create_pdf(pdf_filename, quest_ans)
    print(f"PDF '{pdf_filename}' created successfully.")

    # store these q/a in questions db.
    save_quests_url = "http://127.0.0.1:8000/questions/bulk"
    questions_answers={"questions":questions_answers}
    resp_save_quests = requests.post(save_quests_url,json=questions_answers)
    if resp_save_quests.status_code == 200:
        questions_saved = resp_save_quests.json()
        print("Saved questions are:", questions_saved)
    else:
        print("Failed to get saved user:", resp_save_quests.status_code)


    # Read Doc and creat DB from 
    ## Interview Bot:
    doc = pdf_doc_loader('interview.pdf')
    db = vector_database_creation(doc)
    query = query_database(db=db,job_role=job_role) # Enter Role here 
    ques = query.split("\n") # questions lists

    ques_ans = [] # Ques ans pairs
    for i, q in enumerate(ques):
        ans = input(f"{q}\nAnswer: ")
        # ques_ans.append((q, f"A{i+1}:" + " " + ans))
        answered_at = datetime.datetime.now()
        answered_at = answered_at.strftime("%Y-%m-%d %H:%M:%S")    
        question_data = {"statement":q,"answer":ans,"interview_id":new_interview["id"],"created_at":answered_at}
        ques_ans.append(question_data)

elif option=="2":
    fine_tuned_gpt3 = input("Enter fine-tuned model key: ")
    fine_tune_prompt = input("enter prompt")
    query = query_db_gpt3(fine_tuned_gpt3, fine_tune_prompt)
    ques = query.split("\n") # questions lists

    ques_ans = [] # Ques ans pairs
    for i, q in enumerate(ques):
        ans = input(f"{q}\nAnswer: ")
        # ques_ans.append((q, f"A{i+1}:" + " " + ans))
        answered_at = datetime.datetime.now()
        answered_at = answered_at.strftime("%Y-%m-%d %H:%M:%S")    
        question_data = {"statement":q,"answer":ans,"interview_id":new_interview["id"],"created_at":answered_at}
        ques_ans.append(question_data)

elif option=="3":
    model_name = input("Enter the model from HuggingFace: ")
    pipe = load_Llama2(model_name)

    fine_tune_prompt = input("enter prompt: ")
    query = query_db_llama2(pipe, fine_tune_prompt)
    print(query)
    ques = query.split("\n") # questions lists

    ques_ans = [] # Ques ans pairs
    for i, q in enumerate(ques):
        ans = input(f"{q}\nAnswer: ")
        # ques_ans.append((q, f"A{i+1}:" + " " + ans))
        answered_at = datetime.datetime.now()
        answered_at = answered_at.strftime("%Y-%m-%d %H:%M:%S")    
        question_data = {"statement":q,"answer":ans,"interview_id":new_interview["id"],"created_at":answered_at}
        ques_ans.append(question_data)
else: 
    print("Kinldy select the model number between 1 to 3.")
save_quests_url = "http://127.0.0.1:8000/questions/bulk"
questions_answers={"questions":ques_ans}
resp_save_quests = requests.post(save_quests_url,json=questions_answers)
if resp_save_quests.status_code == 200:
    questions_saved = resp_save_quests.json()
    print("saved questions are:", questions_saved)
else:
    print("Failed to get saved user:", resp_save_quests.status_code)