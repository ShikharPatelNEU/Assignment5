import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title="Insight Engine", page_icon=":money_with_wings:", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Knowledge Summary Generation", "Question Generation", "Similarity Search"])

    st.title("Insight Engine 🤖")

    if page == "Question Generation":
        from question_answer import main as qa_main
        qa_main()
    elif page == "Knowledge Summary Generation":
        from knowledge_summary import main as ks_main
        ks_main()
    elif page == "Similarity Search":
        from similarity_search import app as ss_app
        ss_app()

if __name__ == "__main__":
    main()
