from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

st.session_state["OPENAI_API_KEY"] = st.text_input("이곳에 API KEY를 입력")

if st.session_state.get("OPENAI_API_KEY", ""):
    client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        with st.chat_message("assistant"):
            response = client.responses.create(
                model="gpt-5",
                reasoning={"effort": "high"},
                input=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            st.write(response.output_text)
        st.session_state.messages.append({"role": "assistant", "content": response.output_text})
