import os
import openai
import pandas as pd
import streamlit as st
import boto3
from io import BytesIO

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set up AWS credentials
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Set up S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
BUCKET_NAME = "assignment-5-7245"
OBJECT_KEY = "Team05.csv"

# Load the CSV file from S3
obj = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
df = pd.read_csv(obj['Body'])

# Function to generate questions and answers
def generate_qa(summary, learningoutcomes, num_questions):
    set_a = ""
    set_b = ""

    for i in range((num_questions + 9) // 10):
        start_index = i * 10 + 1
        end_index = min((i + 1) * 10, num_questions)
        prompt = f"Create {end_index - start_index + 1} multiple-choice questions for a financial analyst with an MBA from summary section based on learning outcomes: {learningoutcomes}. Include 4 options per question with one correct answer and immediate answers, maintaining uniform complexity. Make sure to include tables, formulas and relevant information if necessary. Start the numberings from {start_index} to {end_index}."

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=3649,
            n=1,
            stop=None,
            temperature=0.49,
        )

        set_a += response.choices[0].text.strip() + "\n\n" # type: ignore

        prompt = f"Create {end_index - start_index + 1} multiple-choice questions for a financial analyst with an MBA from summary section based on learning outcomes: {learningoutcomes}. Include 4 options per question with one correct answer and immediate answers, maintaining uniform complexity. Make sure to include tables, formulas and relevant information if necessary. The questions should be elaborate. Start the numberings from {start_index} to {end_index}."

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=3649,
            n=1,
            stop=None,
            temperature=0.49,
        )

        set_b += response.choices[0].text.strip() + "\n\n" # type: ignore

    return set_a.strip(), set_b.strip()

def main():
    st.title("Question Generation")

    summary = df["Summary"][0]
    learningoutcomes = df["Learning Outcomes"][0]

    num_questions = st.slider("Number of Questions", 0, 150, 50, step=10)

    if st.button("Generate Q/A Set A"):
        set_a, _ = generate_qa(summary, learningoutcomes, num_questions)
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        set_a_path = os.path.join(downloads_dir, "set_a.txt")
        with open(set_a_path, "w", encoding="utf-8") as f:
            f.write(set_a)
        st.success(f"Set A file saved to: {set_a_path}")

        # Display the generated questions and answers
        st.markdown("### Generated Questions and Answers (Set A)")
        st.text(set_a)

        # Upload the file to S3
        s3_file_key = "set_a.txt"
        s3.put_object(Body=set_a.encode('utf-8'), Bucket=BUCKET_NAME, Key=s3_file_key)
        st.success(f"Set A file uploaded to S3 bucket {BUCKET_NAME} with key {s3_file_key}")

        # Download the file from S3
        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_file_key)
        file_content = file_obj['Body'].read()
        with open(set_a_path, "wb") as f:
            f.write(file_content)
        st.success(f"Set A file downloaded from S3 and saved to: {set_a_path}")

    if st.button("Generate Q/A Set B"):
        _, set_b = generate_qa(summary, learningoutcomes, num_questions)
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        set_b_path = os.path.join(downloads_dir, "set_b.txt")
        with open(set_b_path, "w", encoding="utf-8") as f:
            f.write(set_b)
        st.success(f"Set B file saved to: {set_b_path}")

        # Display the generated questions and answers
        st.markdown("### Generated Questions and Answers (Set B)")
        st.text(set_b)

        # Upload the file to S3
        s3_file_key = "set_b.txt"
        s3.put_object(Body=set_b.encode('utf-8'), Bucket=BUCKET_NAME, Key=s3_file_key)
        st.success(f"Set B file uploaded to S3 bucket {BUCKET_NAME} with key {s3_file_key}")

        # Download the file from S3
        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_file_key)
        file_content = file_obj['Body'].read()
        with open(set_b_path, "wb") as f:
            f.write(file_content)
        st.success(f"Set B file downloaded from S3 and saved to: {set_b_path}")

if __name__ == "__main__":
    main()