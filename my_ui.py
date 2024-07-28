import streamlit as st
from dummy_main import get_retreivial_chain,handle_file_upload,handle_youtube_url
# from Not_main import handle_file_upload,get_response
# from docx import Document 
import os 
# import random
import time 

def response_generator(upload_option,url,prompt):
    print("sending data to model")
    response = get_retreivial_chain(upload_option,url,prompt)
    print("printing response")
    print(type(response))
    for word in response.split():
        yield word + " "
        time.sleep(0.05)



def main():
    st.title("QA Bot")
    
    # Sidebar with file upload options
    st.sidebar.title("Upload Options")
    upload_option = st.sidebar.radio(
        "Select upload type:",
        ('Document', 'URL', 'YouTube', 'Image')
    )

    if upload_option == 'Document':
        file = st.sidebar.file_uploader("Upload a document", type=['txt', 'pdf', 'docx','ppt'])
        url=handle_file_upload(file)
        # url=handle_file_upload(upload_option,file)
    elif upload_option == 'URL':
        url = st.sidebar.text_input("Enter URL")
    elif upload_option == 'YouTube':
        url = st.sidebar.text_input("Enter YouTube link")
        # url = handle_youtube_url(youtube_link)
        # url=handle_file_upload(upload_option,youtube_link)
    elif upload_option == 'Image':
        image = st.sidebar.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])
        url = handle_file_upload(image)
        # url=handle_file_upload(upload_option,image)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            try:
                response = st.write_stream(response_generator(upload_option,url,prompt))
                st.session_state.messages.append({"role": "assistant", "content": response})
            except:
                response="Some eror caused!!"
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        # Add assistant response to chat history
        
if __name__ == "__main__":
    main()
