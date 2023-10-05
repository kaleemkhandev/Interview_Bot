from utils2 import pdf_doc_loader
from utils2 import vector_database_creation
from utils2 import query_database
# from doc_creation import create_pdf

def main():
    
    ## Interview Bot:
    doc = pdf_doc_loader('interview.pdf')
    db = vector_database_creation(doc)

    query = query_database(db=db,job_role="Buisness Development") # Enter Role here 
    
    ques = query.split("\n")
   
    ques_ans = []
    for i, q in enumerate(ques):
        ans = input("Answer: ")
        ques_ans.append((q, f"A{i+1}:" + " " + ans))

    return ques_ans

    
if __name__ == "__main__":
    main()