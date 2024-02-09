from docx import Document
import streamlit as st
import json
import openai
import requests
from openai import OpenAI
import os
import json
import shutil
from io import StringIO
import ast
import re
import random
import time
import requests
from PIL import Image
import json
from prompts import *
from utils import *

if 'blocked_tab2' not in st.session_state:
    st.session_state['blocked_tab2'] = True

if 'blocked_tab3' not in st.session_state:
    st.session_state['blocked_tab3'] = True

if 'isDisabled_btn1' not in st.session_state:
    st.session_state['isDisabled_btn1'] = False

def unblock(tab):
    st.session_state['blocked_tab' + str(tab)] = False

def switch_btn_disabled(tab, value):
    st.session_state['isDisabled_btn' + str(tab)] = value

def generate_title():
    time.sleep(5)
    return 'THIS IS THE TITLE'

openai.api_key = "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"

tab1, tab2, tab3 = st.tabs(["Step1", "Step 2", "Step 3"])



with tab1:
    st.title("Step 1: Generate Titles")
    st.write("Enter the main keyword and supporting keywords to generate titles")
    main_keyword = st.text_input("Main Keyword")
    if st.button("Generate Titles",key='btn1', disabled=st.session_state['isDisabled_btn1']):
        switch_btn_disabled(1, True)
        with st.spinner('Generating Titles...'):
            title = generate_title()
            switch_btn_disabled(1, False)
            # titles = generate_titles(main_keyword, supporting_keywords)
            st.write(title)
            if(title):
                unblock(2)
                st.write("Go to tab 2")
        

    
    
if not st.session_state['blocked_tab2']:
    with tab2:
        st.title("Step 2: Generate Subtitles")
        st.write("Enter the blog title to generate subtitles")
        blog_title = st.text_input("Blog Title")
        if st.button("Generate Subtitles"):
            # subtitles = generate_subtitles(blog_title)
            st.write(blog_title)


with tab3:
    st.title("Step 3: Generate Content")
    st.write("Enter the main title and subtitle to generate content")
    main_title = st.text_input("Main Title")
    subtitle = st.text_input("Subtitle")
    if st.button("Generate Content"):
        # content = generate_content(main_title, subtitle)
        st.write(main_title, subtitle)

