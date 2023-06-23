# # reference
# https://github.com/mobarski/ask-my-pdf/blob/main/src/gui.py
# https://medium.com/@ajvikram/streamlit-gpt-run-free-open-chat-gpt-4-gpt4all-j-with-streamlit-8c467d1c4b5a
# https://blog.streamlit.io/host-your-streamlit-app-for-free/

import streamlit as st
from streamlit_option_menu import option_menu
from utils import generate_chatGPT_prompt
from utils import generate_appraisal
import os

ss = st.session_state
st.set_page_config(layout='wide')
ss["disabled"]=True

# link up streamlit and css
folder_path = os.path.dirname(__file__)
cssfile_path = os.path.join(folder_path, "styles.css")
with open(cssfile_path) as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


def clear_text():
    ss['achievement'] = ""
    ss['strength'] = ""
    ss['weakness'] = ""
    ss['overall_perf_score'] = 3

def clear_text_openai():
    ss['achievement_openai'] = ""
    ss['strength_openai'] = ""
    ss['weakness_openai'] = ""
    ss['overall_perf_score_openai'] = 3
    ss['api_key'] = ""

# sidebar
with st.sidebar:

    choose = option_menu("Appraisal GPT", [ "Generate Appraisal", "Generate Prompt"],
       icons=['pencil', 'chat-square'],
       menu_icon="pass", default_index=0,
       styles={
       "container": {"padding": "5!important", "background-color": "#262730"},
       "icon": {"color": "#02ab21", "font-size": "25px"},
       "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
       "--hover-color": "#56755c"},
       "nav-link-selected": {"background-color": "#2f5335"},
       }
       )

    st.divider()
    st.write("## About Appraisal GPT")
    st.write("version 1.0") 
    st.write("""This application generates suitable prompts to 
       write appraisals with OpenAI API or ChatGPT. """)
    st.write("Made by Ang Wei Jian.") 
    st.write("Source code can be found [here](https://github.com/).", unsafe_allow_html=True)

# Page on "Generate Prompt"
if choose == "Generate Prompt":
    st.markdown('<p class="main-header-text">Generate ChatGPT Prompt for Appraisal Writing:</p>', unsafe_allow_html=True)
    st.write("Follow the steps below to generate a suitable prompt. \
        \nCopy and paste the prompt into the [ChatGPT interface](https://chat.openai.com/) to write your appraisal.", unsafe_allow_html=True)

    st.write('#### Step 1. How positive should the appraisal be?')
    st.slider('1 being the most negative :thumbsdown: \
        \n5 being the most positive :thumbsup:', 1, 5, 3, key='overall_perf_score')

    st.write('#### Step 2. Enter your achievement(s)')
    st.text_area('achievement', key='achievement', height=100, placeholder='Enter your achievement(s) here. Leave blank if none. \
       \ne.g. won first prize in Business Case Competition 2021',
       help='', label_visibility="collapsed", disabled = False)

    st.write('#### Step 3. Enter your strength(s)')
    st.text_area('strength', key='strength', height=100, placeholder='Enter your strength(s) here. Leave blank if none. \
       \ne.g. thorough, team player, responsible, assertive, leader, reliable, proactive, professional, innovative, punctual, \
       efficient, good communicator, positive', 
       help='', label_visibility="collapsed", disabled = False)

    st.write('#### Step 4. Enter your weakness(es)')
    st.text_area('weakness', key='weakness', height=100, placeholder='Enter your weakness(es) here. Leave blank if none. \
       \ne.g. careless, selfish, indecisive, easily swayed ,unreliable, lacks initiative, unprofessional, resistant to change, late, \
       lazy, disinterested', 
       help='', label_visibility="collapsed", disabled = False)

    st.write('#### Step 5. Generate Prompt and Pass into [ChatGPT interface](https://chat.openai.com/)', unsafe_allow_html=True)

    c1,c2= st.columns([1,4])

    if c1.button('Generate Prompt', disabled=False):
       with st.spinner('Preparing Prompt'):
          achievement = ss.get('achievement')
          strength = ss.get('strength')
          weakness = ss.get('weakness')
          overall_perf_score = ss.get('overall_perf_score')
          prompt = generate_chatGPT_prompt(overall_perf_score, strength, achievement, weakness)
          # prompt = ':blue[' + prompt + ']'
          st.divider()
          st.markdown(f'<p class="output-text">{prompt}</p>', unsafe_allow_html=True)

    c2.button("Reset", on_click = clear_text)

# Page on "Generate Appraisal"
elif choose == "Generate Appraisal":
    st.markdown('<p class="main-header-text">Generate Appraisal:</p>', unsafe_allow_html=True)
    st.write("Follow the steps below to write an appraisal.")

    st.write('#### Step 0. Enter your own OpenAI API Key')
    st.text_input('You have to enter your own OpenAI API Key before continuing. \
      You can sign up to OpenAI and/or create your API key [here](https://platform.openai.com/account/api-keys).', key="api_key", 
      placeholder='Enter your OpenAI API key here.', type='password')

    if st.button('I have entered my API Key', disabled=False):
         if ss['api_key'].strip()=="":
            ss["disabled"]=True
         else:
            ss["disabled"]=False

    st.write('#### Step 1. How positive should the appraisal be?')
    st.slider('1 being the most negative :thumbsdown: \
        \n5 being the most positive :thumbsup:', 1, 5, 3, key='overall_perf_score_openai', disabled=ss["disabled"])

    st.write('#### Step 2. Enter your achievement(s)')
    st.text_area('achievement_openai', key='achievement_openai', height=100, placeholder='Enter your achievement(s) here. Leave blank if none. \
       \ne.g. won first prize in Business Case Competition 2021',
       help='', label_visibility="collapsed", disabled=ss["disabled"])

    st.write('#### Step 3. Enter your strength(s)')
    st.text_area('strength_openai', key='strength_openai', height=100, placeholder='Enter your strength(s) here. Leave blank if none. \
       \ne.g. thorough, team player, responsible, assertive, leader, reliable, proactive, professional, innovative, punctual, \
       efficient, good communicator, positive', 
       help='', label_visibility="collapsed", disabled=ss["disabled"])

    st.write('#### Step 4. Enter your weakness(es)')
    st.text_area('weakness_openai', key='weakness_openai', height=100, placeholder='Enter your weakness(es) here. Leave blank if none. \
       \ne.g. careless, selfish, indecisive, easily swayed ,unreliable, lacks initiative, unprofessional, resistant to change, late, \
       lazy, disinterested', 
       help='', label_visibility="collapsed", disabled=ss["disabled"])

    st.write('#### Step 5. Generate Appraisal')

    c3,c4= st.columns([1,4])

    if c3.button('Generate Appraisal', disabled=ss["disabled"]):
       with st.spinner('Preparing Appraisal'):
          achievement = ss.get('achievement_openai')
          strength = ss.get('strength_openai')
          weakness = ss.get('weakness_openai')
          overall_perf_score = ss.get('overall_perf_score_openai')
          api_key = ss.get('api_key')
          try:
            appraisal = generate_appraisal(api_key, overall_perf_score, strength, achievement, weakness)
            st.divider()
            st.markdown(f'<p class="output-text">{appraisal}</p>', unsafe_allow_html=True)
          except Exception:
            st.error('Please enter a valid OpenAI API Key!')
          

    c4.button("Reset", on_click = clear_text_openai)


# upload on github + combine w streamlit (try using desktop git app too)
# test out prompt with different temperature setting
# try app with openAI API key




