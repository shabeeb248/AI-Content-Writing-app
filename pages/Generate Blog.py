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

openai.api_key = OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

client = openai

if 'keyword_input' not in st.session_state:
  st.session_state["keyword_input"]=''

if 'manual_input' not in st.session_state:
  st.session_state["manual_input"]=''

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

if 'additional_info_blog' not in st.session_state:
    st.session_state['additional_info_blog'] = ''

if 'manual_input_visible' not in st.session_state:
    st.session_state['manual_input_visible'] = False

if 'google_search_full_data' not in st.session_state:
    st.session_state['google_search_full_data'] = None

if 'introduction' not in st.session_state:
    st.session_state['introduction'] = None

if 'conclusion' not in st.session_state:
    st.session_state['conclusion'] = None

def unblock(tab):
    st.session_state['blocked_tab' + str(tab)] = False


openai.api_key = "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"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Step1", "Step 2", "Step 3", "Step 4", "Step 5"])



with tab1:
    st.title('Step1 : Enter your keyword')
    st.session_state["keyword_input"] = st.text_input("Enter a keyword", key="search_keyword")
    if not st.session_state["keyword_input"]:
            st.error("Please fill out the keyword field")
    else:
        if st.button('Generate Search words'):
            with st.spinner('Generating...'):
                print('getting google search')
                data=get_google_serach(st.session_state["keyword_input"])
                st.session_state['google_search_full_data'] = data
        if st.session_state['google_search_full_data']:
            google_keywords=[]
            main_categories = ['related_searches', 'related_questions','organic_results']
            #checkbox to select categories
            checked_categories = st.multiselect("Select categories", main_categories, key="categories")
            # st.write(checked_categories)
            data = st.session_state['google_search_full_data']
            if st.button('Add Selected Categories'):
                for category in checked_categories:
                    for item in data[category]:
                        if 'title' in item and item['title'] not in st.session_state['google_keywords']:
                            google_keywords.append(item['title'])
                        if 'query' in item and item['query'] not in st.session_state['google_keywords']:
                            google_keywords.append(item['query'])
                st.success(f"Keywords added")
                # for category in main_categories:
                #     checked = st.checkbox(category, key=category)
                #     if checked:
                #         che
                    # if st.checkbox(category, key=category):
                    #     for item in data[category]:
                    #         if 'title' in item:
                    #             google_keywords.append(item['title'])
                    #         if 'query' in item:
                    #             google_keywords.append(item['query'])
                # st.write(st.session_state['google_search_full_data'].keys())
                # data = json.loads(data)
                # google_keywords=[]
                # for item in data['organic']:
                #     if 'title' in item:
                #         google_keywords.append(item['title'])

            for search in data['related_searches']:
                if 'title' in search:
                    google_keywords.append(search['title'])
            
            st.session_state['google_keywords'].extend(list(dict.fromkeys(google_keywords)))
            print("GOOGLE KEYWORDS", st.session_state['google_keywords'])
            if(data) and not st.session_state.get('unblocked_tab2_1', False):
                unblock(2)
                st.session_state['unblocked_tab2_1'] = True
        if st.button('Add Your Search Words'):
            st.session_state['manual_input_visible'] = True
        if st.session_state['manual_input_visible']:
            st.session_state["manual_input"]= st.text_input("Enter your search words here",key='manual_input_1')
            if st.button("Add"):
                if 'google_keywords' not in st.session_state:
                    st.session_state['google_keywords'] = []
                st.session_state['google_keywords'].append(st.session_state['manual_input'])
                st.success(f"Keyword '{st.session_state['manual_input']}' added")
                if st.session_state['google_keywords'] and not st.session_state.get('unblocked_tab2_2', False):  
                    unblock(2)
                    st.session_state['unblocked_tab2_2'] = True
    if st.session_state.get('unblocked_tab2_1', False) or st.session_state.get('unblocked_tab2_2', False):
        st.markdown("<h3 style='color:blue; txt-align:center;'>Go to tab 2</h3>", unsafe_allow_html=True)
               
        

    
    
if not st.session_state['blocked_tab2']:
    with tab2:
        st.title("Step 2: Select Keywords")
        st.subheader("Please select one or more appropriate keywords:")
        if st.session_state['google_keywords']:
            for item in st.session_state['google_keywords']:
                if st.checkbox(item, key='keyword-'+item):
                    if 'selected_items' not in st.session_state:
                        st.session_state['selected_items'] = []
                    st.session_state['selected_items'].append(item)
        if not st.session_state['selected_items']:
                st.error("Please select multiple keywords")
        else:
            additional_info = st.text_area("Additional Info:", placeholder="Enter any additional information for generating the title here.")
       
            print('items selected')
            # Input box add - Additional Instructions 
            if st.button('Generate Titles'):
                with st.spinner('Generating...'):
                    print('submit btn clicked')
                    titles_10=get_titles_based_on_keyword(prompt_1,st.session_state["keyword_input"],st.session_state['selected_items'],additional_info)
                    if isinstance(titles_10, list):
                        st.session_state['titles_10']=titles_10
                    if(titles_10):
                        unblock(3)
                        st.markdown("<h3 style='color:blue; txt-align:center;'>Go to tab 3</h3>", unsafe_allow_html=True)



if not st.session_state['blocked_tab3']:
    with tab3:
        st.title("Step 3: Choose title")
        if st.session_state['titles_10']:
            if st.button('Regenerate Titles'):
                with st.spinner('Generating...'):
                    titles_10=get_titles_based_on_keyword(prompt_1,st.session_state["keyword_input"],st.session_state['selected_items'],additional_info)
            print(st.session_state['titles_10'])
            st.session_state['final_title']=st.radio('Choose a title: ', options=st.session_state['titles_10'], key='radio_title')
        if st.session_state['final_title']:
            additional_info_subtitles = st.text_area("Additional Info:", placeholder="Enter any additional information for generating the subtitles here.")
            # btn_name = 'Generate New Subtitles' if st.session_state['subtitles'] else 'Generate Subtitles'
            if st.button('Generate Subtitles', key='generate_subtitles_button'):
                with st.spinner('Generating...'):
                    st.session_state['subtitles']=create_subtitles(st.session_state['final_title'], additional_info_subtitles)
                    if(st.session_state['subtitles']):
                        unblock(4)
                        st.markdown("<h3 style='color:blue; txt-align:center;'>Go to tab 4</h3>", unsafe_allow_html=True)

if not st.session_state['blocked_tab4']:
    with tab4:
        st.title("Step 4: Generate Subtitle")
        if (st.session_state['subtitles']):
            if st.button('Generate new subtitles' , key='regenerate_subtitles'):
                with st.spinner('Generating...'):
                    st.session_state['subtitles']=create_subtitles(st.session_state['final_title'], additional_info_subtitles)
            for i in st.session_state['subtitles']:
                st.write(i)
            additional_info_blog = st.text_area("Additional Info:", placeholder="Enter any additional information for generating the blog here.")
            st.session_state['additional_info_blog'] = additional_info_blog
            if st.button('Generate Blog'):  
                with st.spinner('Generating...'):
                    deleteOutput("output")
                    createFolders("output")
                    # add_image(st.session_state['final_title'])
                    # content, introduction, conclusion
                    st.session_state['blog'], st.session_state['introduction'], st.session_state['conclusion']=generate_blog(st.session_state['final_title'],st.session_state['subtitles'], additional_info_blog)
                    print(st.session_state['blog'])
                    print("INTRO", st.session_state['conclusion'])
                    # print("CONCLUSION", conclusion)
                    if(st.session_state['blog']):
                        unblock(5)
                        st.markdown("<h3 style='color:blue; txt-align:center;'>Go to tab 5</h3>", unsafe_allow_html=True)


if not st.session_state['blocked_tab5']:
    with tab5:
        st.title('Last Step : Generate Blog')
        if st.session_state['subtitles']:
            if st.button('Regenerate Blog', key='regenerate_blog_button'):  
                st.session_state['pdf_ready'] = False
                with st.spinner('Generating...'):
                    deleteOutput("output")
                    createFolders("output")
                    # add_image(st.session_state['final_title'])
                    st.session_state['blog'], st.session_state['introduction'], st.session_state['conclusion']=generate_blog(st.session_state['final_title'],st.session_state['subtitles'], st.session_state['additional_info_blog'])
        blog_data = {
            'Title': st.session_state['final_title'], 
            'blog': st.session_state['blog'],
            'introduction':   st.session_state['introduction'],
            'conclusion': st.session_state['conclusion']
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
            st.markdown(f"<div style='margin-left: 20px; margin-bottom: 20px;'>{st.session_state['introduction']}</div>", unsafe_allow_html=True)
            for i in st.session_state['blog']:
                st.markdown(f"<h4 style='font-weight: 400;'>{i['subtitle']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<div style='margin-left: 20px; margin-bottom: 20px;'>{i['text']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-left: 20px; margin-bottom: 20px;'>{st.session_state['conclusion']}</div>", unsafe_allow_html=True)

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

