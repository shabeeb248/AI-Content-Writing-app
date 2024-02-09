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

if 'keyword_input' not in st.session_state:
  st.session_state["keyword_input"]=''

if 'final_title' not in st.session_state:
  st.session_state["final_title"]=''

if 'subtitles' not in st.session_state:
  st.session_state["subtitles"]=''

if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

if 'selected_items' not in st.session_state:
    st.session_state['selected_items'] = []

if 'selected_titles' not in st.session_state:
    st.session_state['selected_titles'] = []

if 'google_keywords' not in st.session_state:
    st.session_state['google_keywords'] = []


if 'titles_10' not in st.session_state:
    st.session_state['titles_10'] = []   

if 'blog' not in st.session_state:
    st.session_state['blog'] = None 

if 'blog_data' not in st.session_state:
    st.session_state['blog_data'] = None 

if 'generation_in_progress' not in st.session_state:
    st.session_state['generation_in_progress'] = False

if "pdf_ready" not in st.session_state:
    st.session_state['pdf_ready'] = False

if 'blocked_tab2' not in st.session_state:
    st.session_state['blocked_tab2'] = True

if 'blocked_tab3' not in st.session_state:
    st.session_state['blocked_tab3'] = True

if 'blocked_tab4' not in st.session_state:
    st.session_state['blocked_tab4'] = True

if 'blocked_tab5' not in st.session_state:
    st.session_state['blocked_tab5'] = True

if 'isDisabled_btn1' not in st.session_state:
    st.session_state['isDisabled_btn1'] = False

def unblock(tab):
    st.session_state['blocked_tab' + str(tab)] = False


openai.api_key = "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"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Step1", "Step 2", "Step 3", "Step 4", "Last Step"])



with tab1:
    st.title('Step1 : Enter your keyword')
    st.session_state["keyword_input"] = st.text_input("Enter a keyword")
    if not st.session_state["keyword_input"]:
            st.error("Please fill out the keyword field")
    else:
        if st.button('Generate Search words'):
            with st.spinner('Generating...'):
                print('getting google search')
                data=get_google_serach(st.session_state["keyword_input"])
                data = json.loads(data)
                google_keywords=[]
                for item in data['organic']:
                    if 'title' in item:
                        google_keywords.append(item['title'])

            for search in data['related_searches']:
                if 'title' in search:
                    google_keywords.append(search['title'])
            
            st.session_state['google_keywords'] = list(dict.fromkeys(google_keywords))
            print("GOOGLE KEYWORDS", st.session_state['google_keywords'])
    # st.title("Step 1: Generate Titles")
    # st.write("Enter the main keyword and supporting keywords to generate titles")
    # main_keyword = st.text_input("Main Keyword")
    # if st.button("Generate Titles",key='btn1'):
    #     with st.spinner('Generating Titles...'):
    #         title = generate_title()
    #         # titles = generate_titles(main_keyword, supporting_keywords)
    #         st.write(title)
            if(data):
                unblock(2)
                st.write("Go to tab 2")
        

    
    
if not st.session_state['blocked_tab2']:
    with tab2:
        st.title("Step 2: Select Keywords")
        st.subheader("Please select one or more appropriate keywords:")
        if st.session_state['google_keywords']:
            for item in st.session_state['google_keywords']:
                if st.checkbox(item, key='keyword-'+item):
                    st.session_state['selected_items'].append(item)
        if not st.session_state['selected_items']:
                st.error("Please select multiple keywords")
        else:
            print('items selected')
            # Input box add - Additional Instructions 
            if st.button('Generate Titles'):
                with st.spinner('Generating...'):
                    print('submit btn clicked')
                    titles_10=get_titles_based_on_keyword(prompt_1,st.session_state["keyword_input"],st.session_state['selected_items'])
                    if isinstance(titles_10, list):
                        st.session_state['titles_10']=titles_10
                    if(titles_10):
                        unblock(3)
                        st.write("Go to tab 3")


if not st.session_state['blocked_tab3']:
    with tab3:
        st.title("Step 3: Choose title")
        if st.session_state['titles_10']:
            st.session_state['final_title']=st.radio('Choose a title: ', options=st.session_state['titles_10'], key='radio_title')
        if st.session_state['final_title']:
            # btn_name = 'Generate New Subtitles' if st.session_state['subtitles'] else 'Generate Subtitles'
            if st.button('Generate Subtitles', key='generate_subtitles_button'):
                with st.spinner('Generating...'):
                    st.session_state['subtitles']=create_subtitles(st.session_state['final_title'])
                    if(st.session_state['subtitles']):
                        unblock(4)
                        st.write('go to tab4')

if not st.session_state['blocked_tab4']:
    with tab4:
        st.title("Step 4: Generate Subtitle")
        if (st.session_state['subtitles']):
            if st.button('Generate new subtitles' , key='regenerate_subtitles'):
                with st.spinner('Generating...'):
                    st.session_state['subtitles']=create_subtitles(st.session_state['final_title'])
            for i in st.session_state['subtitles']:
                st.write(i)
            if st.button('Generate Blog'):  
                with st.spinner('Generating...'):
                    deleteOutput("output")
                    createFolders("output")
                    # add_image(st.session_state['final_title'])
                    st.session_state['blog']=generate_blog(st.session_state['subtitles'])
                    if(st.session_state['blog']):
                        unblock(5)
                        st.write('go to the last tab')

if not st.session_state['blocked_tab5']:
    with tab5:
        st.title('Last Step : Gnerate Blog')
        if st.session_state['subtitles']:
            if st.button('Regenerate Blog', key='regenerate_blog_button'):  
                with st.spinner('Generating...'):
                    deleteOutput("output")
                    createFolders("output")
                    # add_image(st.session_state['final_title'])
                    st.session_state['blog']=generate_blog( st.session_state['subtitles'])
        blog_data = {
            'Title': st.session_state['final_title'], 
            'blog': st.session_state['blog'],  
        }
        # Add image path to blog_data
        # image_path = 'output/img.jpg'  # Adjust the image path as per your file structure
        # blog_data['image_path'] = image_path

        # Store blog_data in session state
        st.session_state['blog_data'] = blog_data       
        if st.session_state['blog']:
            # print(st.session_state["blog"])
            st.markdown(f"<h1 style='font-weight: bold; text-align:center;'>{st.session_state['final_title']}</h2>", unsafe_allow_html=True)
            # st.image('output/img.jpg',  use_column_width='always')
            for i in st.session_state['blog']:
                st.markdown(f"<h4 style='font-weight: 400;'>{i['subtitle']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<div style='margin-left: 20px; margin-bottom: 20px;'>{i['text']}</div>", unsafe_allow_html=True)
            if st.button("Generate PDF"):
                st.session_state['generation_in_progress'] = True
                with st.spinner('Generating...'):
                    x = generate_pdf(st.session_state['blog_data'])
                    if(x):
                        st.session_state['pdf_ready']=True

        if st.session_state['pdf_ready']:
                # Download PDF file
            file_name = st.session_state['final_title']+'.pdf'
            with open("output/blog.pdf", "rb") as file:
                st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name=file_name,
                    mime="application/pdf"
                )

