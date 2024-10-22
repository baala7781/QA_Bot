from langchain_community.document_loaders import UnstructuredPDFLoader
import io

import streamlit as st
st.title("Document similarity")

input_option = st.selectbox("How do you want to input the Job Description?", ("Enter URL", "Enter Text"),index=None,)

if input_option == "Enter URL":
    job_description_url = st.text_input("Enter the Job Description URL")
else:
    job_description_text = st.text_area("Enter the Job Description Text")

resumes = st.file_uploader("Upload Resumes (PDFs only)", type=["pdf"], accept_multiple_files=True)
# if resumes:
#     for resume in resumes:
#         resume_data=io.BytesIO(resume.read())
#         print(resume_data)
#         loader=UnstructuredPDFLoader(resume_data)
#         data=loader.load()
        # print(data)
if st.button("Submit"):
    st.write("Processing your input...")
