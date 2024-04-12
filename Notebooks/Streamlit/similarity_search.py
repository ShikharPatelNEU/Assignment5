import streamlit as st
import pandas as pd
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import openai
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from pinecone import Pinecone
import re
from langchain_pinecone import PineconeVectorStore

from app import generate_qa

# Set up OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")
os.environ["PINECONE_API_KEY"] = "7c170d7e-968b-49d4-a798-c28e288d0482"

# Set up Pinecone API key and environment
# pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment=os.environ.get("PINECONE_ENVIRONMENT"))

pc = Pinecone(
    api_key="7c170d7e-968b-49d4-a798-c28e288d0482",
    environment="us-east1-gcp"
)

# Load the data
df = pd.read_csv("Team05.csv")
summary = df["Summary"][0]
learningoutcomes = df["LearningOutcomes"][0]

# Generate questions and answers
set_a, set_b = generate_qa(summary, learningoutcomes)

# Save set_a to a file
with open("set_a.txt", "w", encoding="utf-8") as f:
    f.write(set_a)

# Save set_b to a file
with open("set_b.txt", "w", encoding="utf-8") as f:
    f.write(set_b)

# Print the current working directory
print("Current working directory:", os.getcwd())

# Extract questions and answers from set_a
set_a_lines = set_a.split("\n\n")
set_a_questions = [line.split("\n")[0] for line in set_a_lines]
set_a_answers = [line for line in set_a_lines if "Answer:" in line]
set_a_answers = [line.split("\n")[5] for line in set_a_lines]


# Extract questions and options from set_b
set_b_lines = set_b.split("\n\n")
set_b_questions = [line.split("\n")[0] for line in set_b_lines]
set_b_options = [line.split("\n")[1:5] for line in set_b_lines]
set_b_answer = set_b_answer = [line.split("\n")[5] for line in set_b_lines]

# Set up embeddings
embeddings = OpenAIEmbeddings()

# Set up Pinecone index
index_name = "assignment05"
docsearch = PineconeVectorStore.from_texts(
    set_a_questions,
    embeddings,
    index_name=index_name,
    namespace="questions",
    metadatas=[{"id": i} for i in range(len(set_a_questions))]
)

# Get document IDs from the Pinecone index
index = pc.Index(index_name)
all_ids = [id for ids in index.list(namespace='questions') for id in ids]

docsearch_answers = PineconeVectorStore.from_texts(
    set_a_answers,
    embeddings,
    ids=all_ids,
    index_name=index_name,
    namespace="answers",
    metadatas=[{"question_id": docid} for docid in all_ids]
)

# Streamlit app

def app():
    st.title("Question Search")
    question = st.text_input("Enter a question")
    if st.button("Search Similar Questions"):
        if question:
            set_b_only_questions_vectors = embeddings.embed_query(question)
            question_t3 = index.query(vector=set_b_only_questions_vectors, top_k=3, namespace='questions', include_metadata=True, include_values=True)
            answer_ids = []
            for q in question_t3.matches:
                answer_ids.append(index.query(vector=q.values, top_k=1, namespace='answers', include_metadata=True))
            answers_gpt = []
            for answer_id in answer_ids:
                answers_gpt.append(answer_id.matches[0].metadata['text'])
            gpt4_answer = ask_gpt4(question, set_b_options[0], answers_gpt)
            st.write(f"## Question: {question}")
            st.write(f"### GPT-4 Answer: {gpt4_answer}")
            st.write("### Similar Questions and Answers:")
            for i, (q, a) in enumerate(zip(question_t3.matches, answers_gpt)):
                st.write(f"#### {i+1}. {q.metadata['text']}")
                st.write(f"Answer: {a}")

def ask_gpt4(set_b_question, set_b_answers, set_a_similar_answers):
    prompt = f"""
    Question: {set_b_question}
    Answer choices: {', '.join(set_b_answers)}
    
    The 3 most similar questions and answers from the database are:
    1. {set_a_similar_answers[0][0]}
       Answer: {set_a_similar_answers[0][1]}
    2. {set_a_similar_answers[1][0]}
       Answer: {set_a_similar_answers[1][1]}
    3. {set_a_similar_answers[2][0]}
       Answer: {set_a_similar_answers[2][1]}
    
    Based on the information provided, which answer choice do you think is correct for the question above? in Format as below:
    Answer: C (Answer choice)
    """
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=2600,
        n=1,
        stop=None,
        temperature=0.49,
    )
    
    return response.choices[0].text.strip() # type: ignore

if __name__ == "__main__":
    app()