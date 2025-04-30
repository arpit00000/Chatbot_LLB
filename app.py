import os
from dotenv import load_dotenv

load_dotenv()

from embedchain import App

def chat_llb():
    app = App()
    return app

app = chat_llb()


from unittest import loader
import matplotlib
matplotlib.use('Agg') 
import streamlit as st

from embedchain import App
import queue
import threading
from io import StringIO
from PIL import Image
import os
import requests

from embedchain import App
from embedchain.config import BaseLlmConfig
from embedchain.helpers.callbacks import (StreamingStdOutCallbackHandlerYield,
                                          generate)





# from embedchain import Pipeline as App

@st.cache_resource
def chat_llb():
    app=App()
    return app


link_arr=["https://www.indiacode.nic.in/bitstream/123456789/2338/1/A1882-04.pdf","https://registration.uk.gov.in/files/Stamp_Act_Eng.pdf","https://dolr.gov.in/sites/default/files/THE%20LAND%20ACQUISITION%20ACT.pdf","https://www.indiacode.nic.in/bitstream/123456789/13236/1/the_registration_act%2C_1908.pdf","https://www.indiacode.nic.in/bitstream/123456789/5615/1/muslim_marriages_registration_act%2C_1981.pdf","https://www.indiacode.nic.in/bitstream/123456789/2187/2/A187209.pdf","https://www.icsi.edu/media/webmodules/companiesact2013/COMPANIES%20ACT%202013%20READY%20REFERENCER%2013%20AUG%202014.pdf","https://www.indiacode.nic.in/bitstream/123456789/15351/1/iea_1872.pdf","https://www.iitk.ac.in/wc/data/IPC_186045.pdf","https://lddashboard.legislative.gov.in/sites/default/files/A1955-25_1.pdf","https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2023/05/2023050195.pdf","""https://sclsc.gov.in/theme/front/pdf/ACTS%20FINAL/THE%20CODE%20OF%20CIVIL%20PROCEDURE,%201908.pdf""","https://ncwapps.nic.in/acts/TheIndianChristianMarriageAct1872-15of1872.pdf","https://www.indiacode.nic.in/bitstream/123456789/2347/1/190907.pdf","https://www.indiacode.nic.in/bitstream/123456789/2280/1/A1869-04.pdf","https://www.indiacode.nic.in/bitstream/123456789/15480/1/special_marriage_act.pdf"]


link_arr[9]="https://highcourtchd.gov.in/hclscc/subpages/pdf_files/4.pdf"



@st.cache_resource
def add_data(arr):
    n=len(arr)
    for i in range(n):
        try:
            app.add(arr[i],data_type='pdf_file')
            # print(i,'-> {arr[i]} done')
        except:
            print("missed",i,link_arr[i])
    # app.add("/adv.Basant_22_G", data_type="dropbox")


app=chat_llb()

assistant_avatar_url = "🇮🇳"  # noqa: E501

#adding data into rag
add_data(link_arr)

st.markdown("<h1 style='text-align: center; color: #aaa;'>Chat LLB 👩‍⚖️</h1>", unsafe_allow_html=True)



image_path="https://sc0.blr1.digitaloceanspaces.com/large/829013-51163-wrquznbrhc-1486711910.jpg"

 


styled_caption = '<p style="font-size: 18px; color: #aaa;">🇮🇳 made with love by <a href="https://www.linkedin.com/in/basantsingh1000/">Basant Singh</a> powered by <a href="https://github.com/embedchain/embedchain">Embedchain</a></p>'  # noqa: E501
st.markdown(styled_caption, unsafe_allow_html=True)  

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
Hi, I am Chat LLB your helpful law assistant, I can answer the questions realted to divorce,property & Crime.
Ask one question at a time only

Sample questions:
- What are charges for hit and run?
- How to file a divorce in unilateral way?
- What is article 370 ?
- How to register witness in murder case?
- In B2B transactions how to sue another company?
- Who can grant pardon from sentence ?

It sources knowlege from indian govt🇮🇳 but AI models can hallucinate, Always rely on expert👩‍⚖️.

""",

        }
    ]



prompt_for_llm="""  
  You'r helpful AI assisant given the task to help people seeking law advise.
  You have to help person to use the Indian laws in legal manner.
  Answer in step by step in points by highlighting the sections of indian laws & constitution.
  Refuse to answer if it is not helping in legal affairs, also donot concoat anything.
  $context
  
  Query: $query


  Helpful Answer:
"""

for message in st.session_state.messages:
    role=message['role']
    with st.chat_message(role,avatar=assistant_avatar_url if role == "assistant" else None):
        st.markdown(message["content"])


if prompt := st.chat_input("Pls ask one question at a time. "):
    
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant",avatar=assistant_avatar_url):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""
        q = queue.Queue()
        def app_response(result):
            config = BaseLlmConfig(prompt=prompt_for_llm,stream=True, callbacks=[StreamingStdOutCallbackHandlerYield(q)])
            answer, citations = app.chat(prompt, config=config, citations=True)
            result["answer"] = answer
            result["citations"] = citations

        results = {}
        thread = threading.Thread(target=app_response, args=(results,))
        thread.start()
        for answer_chunk in generate(q):
            full_response += answer_chunk
            msg_placeholder.markdown(full_response)
        
        
        thread.join()
        answer, citations = results["answer"], results["citations"]
        if citations:
            full_response += "\n\n**Sources**:\n"
            sources = list(set(map(lambda x: x[1]["url"], citations)))
            for i, source in enumerate(sources):
                full_response += f"{i+1}. {source}\n"

        msg_placeholder.markdown(full_response)


        st.session_state.messages.append({"role": "assistant", "content": full_response})
    









