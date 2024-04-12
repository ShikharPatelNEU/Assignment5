import os
import openai
import pandas as pd
import streamlit as st
import boto3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set up AWS credentials
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Set up S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
BUCKET_NAME = "assignment-5-7245"

# Function to generate knowledge summary
def generate_knowledge_summary(los):
    prompt = f"Given the following learning outcome statement (LOS):\n\nLOS: {los}\n\nCreate a technical note that summarizes the key LOS. Be sure to include tables, figures, and equations as needed. Format the output in Markdown."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text # type: ignore

def fetch_combined_summary_notes():
    object_key = "combined_summary_notes.md"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
        combined_summary_notes = obj['Body'].read().decode('utf-8')
        return combined_summary_notes
    except Exception as e:
        st.error(f"Error fetching combined summary notes: {e}")
        return None

def main():
    st.title("Knowledge Summary Generation")
    los = st.text_area("Enter the Learning Outcome Statement (LOS)")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Summary"):
            summary_text = generate_knowledge_summary(los)
            st.markdown(f"<div style='text-align: center;'>{summary_text}</div>", unsafe_allow_html=True)

            # Save input and output to a text file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{os.getpid()}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Input LOS:\n{los}\n\nOutput Summary:\n{summary_text}")

            # Upload the text file to S3
            s3.upload_file(filename, BUCKET_NAME, filename)
            st.success(f"Input and output saved to {filename} and uploaded to S3 bucket {BUCKET_NAME}")

            # Remove the local text file
            os.remove(filename)

    with col2:
        if st.button("Combined Technical Note"):
            combined_summary_notes = fetch_combined_summary_notes()
            if combined_summary_notes:
                st.markdown(f"<div style='text-align: center;'>{combined_summary_notes}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()