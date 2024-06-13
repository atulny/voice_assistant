import os

import pyaudio
import streamlit as st
from langchain.memory import ConversationBufferMemory
import re
from utils import record_audio_chunk, transcribe_audio, get_response_llm, play_text_to_speech, load_whisper

chunk_file = 'temp_audio_chunk.wav'
model = load_whisper()
def main():
    st.set_page_config(layout="wide", page_title="Virtual Friends")

    hide_streamlit_style = """
       <style>
       *, html {scroll-behavior: smooth !important;}
           #MainMenu {visibility: hidden;}

       #stDecoration  {visibility: hidden;}

       .stDeployButton{visibility: hidden;}

       header{display:none !important}

       [data-testid="stSidebarUserContent"]{padding-top:.8em;}

       [data-testid="block-container"]{padding-top:1em;}

       footer {visibility: hidden;}
       .block-container {padding:.5rem 4rem !important}

       .header-wrap{border-bottom:1px solid #ccc;background-color:#efefef;
           font-size:150%;padding:0 10px;position:fixed;top:1px;left:1px;width:100%;
           height:3rem;display:flex;
          flex-direction:row;justify-content:space-between;
       }

       .header-wrap .header-right img {height:28px;margin-right:5px;}

       [data-testid="stSidebarNav"] {
           background-size: 240px auto;
           background-repeat: no-repeat;
           background-position:center center !important;
           padding-top:370px !important;
           box-sizing:border;
           margin-top:-150px !important;
       }

       [data-testid='column']:has(.full-length){height:75vh !important}

       [data-testid='column']:has(.shaded){background-color:#f0f2f6;}

       .block-container:has(.header-wrap) > [data-testid='stVerticalBlockBorderWrapper'] >div > [data-testid='stVerticalBlock']{
         margin-top:-200px
       } 

       .element-container > .stMarkdown > [data-testid='stMarkdownContainer'] > .p__h{
           overflow;hidden;height:0  !important;max-height:0  !important;margin:0  !important;padding:0 !important;
       }

       .block-container  .block-container{
           padding:0 !important
       }
 
 
       </style>

       """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown('<h3>AI Friend</h3>', unsafe_allow_html=True)
    cols = st.columns([1,2])
    friend_name =  cols[0].text_input("Friend Name", key="friend_name", value="Jarvis")
    friend_description =  cols[1].text_area("About Friend", key="friend_description",  value="Jarvis is a helpful and loyal assistant.",height=20)

    memory = ConversationBufferMemory(memory_key="chat_history")

    if st.button("Start Conversation/Speak"):
        while True:
            # Audio Stream Initialization
            try:
                os.remove(chunk_file)
            except:
                pass
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

            # Record and save audio chunk
            record_audio_chunk(audio, stream,chunk_file)
            print(f"saving {chunk_file}")

            text = transcribe_audio(model, chunk_file)
            print(f"text {text}")

            if text  and re.sub(r"[\W]","",text).lower() not in ["bye", "stop","goodbye","byebye","tata"]:

                st.markdown(
                    f'<div style="padding: 10px; border-radius: 5px;">Me 👤: {text}</div>',
                    unsafe_allow_html=True)

                try:
                    os.remove(chunk_file)
                except:
                    pass
                response_llm = get_response_llm(user_question=text, memory=memory)
                st.markdown(
                    f'<div style="padding: 10px; border-radius: 5px;">{friend_name.split(" ")[0] or "Assistant"} 🤖: {response_llm}</div>',
                    unsafe_allow_html=True)
                print("playing ... ")

                play_text_to_speech(text=response_llm)
            else:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                break  # Exit the while loop
        print("End Conversation")



if __name__ == "__main__":
    main()