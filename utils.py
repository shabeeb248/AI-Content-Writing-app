
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
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image
import json
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import SimpleDocTemplate,PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer,Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageTemplate, Image, Frame
from reportlab.lib.styles import getSampleStyleSheet
from prompts import *
import string

client = openai

def randomString():
    N = 5
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def deleteOutput(folder):
    if os.path.exists(folder):
        try:
            # Remove the folder and all its contents
            shutil.rmtree(folder)
            print(f"Successfully deleted the folder: {folder}")
        except Exception as e:
            print(f'Failed to delete {folder}. Reason: {e}')
    else:
        print(f"The folder {folder} does not exist.")


def createFolders(dir):
    try:
            if not os.path.exists(dir):
                os.makedirs(dir, exist_ok=True)
                print("DIRECTORIES CREATED")
            #
    except Exception as e:
        ('Failed to create folders  Reason: %s' % ( e))


# def add_image(title):
#     try:
#         prompt = prompt_image.format(title)
#         res=generate_image_e_3(prompt,'img')
#         return res
#     except Exception as e:
#             print(f' Reason: {e}')

def generate_pdf(blog_data):
    print('generate pdf')
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_file = os.path.join(output_folder, "blog.pdf")  
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    border_template = PageTemplate(id='border_template')
    border_margin =20
    page_width, page_height = letter
    content_frame = Frame(border_margin, border_margin, page_width - 2 * border_margin, page_height - 2 * border_margin)

    border_template.frames.append(content_frame)
    story = []

    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        name='Normal',
        fontSize=13,
        leading=17,  # Line spacing, adjust as needed
        textColor='black',  # Text color
        fontName='Helvetica'
    )
    
    title_style = ParagraphStyle(
            name='Title',
            fontSize=26,
            leading=24,  # Line spacing, adjust as needed
            spaceAfter=60,  # Space after each paragraph, adjust as needed
            spaceBefore=40,  # Space before each paragraph, adjust as needed
            alignment=1,  # Centered text
            fontName='Helvetica-Bold'
        )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        fontSize=17,
        spaceAfter=10,  # Space after each paragraph, adjust as needed
        spaceBefore=20,  # Space before each paragraph, adjust as needed
        fontName='Helvetica-Bold'
    )

    # Content style
    content_style = ParagraphStyle(
        name='Content',
        fontSize=13,
        leading=20,  # Line spacing, adjust as needed
        spaceAfter=60,  # Space after each paragraph, adjust as needed
        spaceBefore=40,  # Space before each paragraph, adjust as needed
    )
    centered = ParagraphStyle(
        name="Centered",
        alignment=1,
        fontSize=15,
        fontName="Helvetica-Bold",

    )
    bold = ParagraphStyle(
        name="Bold",
        fontName="Helvetica-Bold",
        fontSize=13,
    )

    # Add title to the document
    text = blog_data["Title"]
    story.append(Spacer(1, 1*inch))
    paragraph = Paragraph(text, title_style)
    story.append(paragraph)
    # image_path = f"output/img.jpg"
    # image = Image(image_path, width=350, height=350)  # Adjust the width and height as needed
    # story.append(image)
    story.append(PageBreak())
    

    # Add subtitles and content to the document
    for item in blog_data['blog']:
        subtitle = Paragraph(item['subtitle'], subtitle_style)
        content = Paragraph(item['text'], content_style)
        story.append(subtitle)
        story.append(content)
        story.append(Spacer(1, 12))  # Add spacing between subtitles
        
    # Build the PDF document
    doc.build(story)
    return ("PDF created successfully")


def create_subtitles(title):
    try:
        # subtitles = ['intro','section a - the beginning','section b - the middle','section c - the end','conclusion']
        # # //return  subtitles in random order
        # return random.sample(subtitles, len(subtitles))
        prompt = prompt_subtitle.format(title)
        res=get_response_from_openai_gpt3_5(prompt)
        print(res)
        start_index = res.find('[') + 1  
        end_index = res.find(']')
        list_str = res[start_index:end_index]
        result_list = [item.strip().strip('"').strip("'") for item in list_str.split(',')]
        return result_list
    except Exception as e:
            print(f' Reason: {e}')
def create_content_for_subtitles(subtitle):
    try:
        prompt = prompt_content.format(subtitle)
        res=get_response_from_openai_gpt3_5(prompt)
        print(res)
        return res
    except Exception as e:
            print(f' Reason: {e}')

# with history            
# def create_content_for_subtitles(title,subtitle,history):
#     try:
#         prompt = prompt_content.format(title,subtitle,history)
#         res=get_response_from_openai_gpt3_5(prompt)
#         print(res)
#         return res
#     except Exception as e:
#             print(f' Reason: {e}')
    

def generate_blog(subtitles):
    content = []
    for i in subtitles:
        blog = create_content_for_subtitles(i)
        x = { 'subtitle':i, 'text':blog}
        content.append(x)
    return content

# with history
    # content = []
    # introduction = "introduction" # Create introduction from openai
    # history = """
    # Title: {title}

    # {introduction}
    # """
    # for i in subtitles:
    #     blog = create_content_for_subtitles(title,i,history)
    #     x = { 'subtitle':i, 'text':blog}
    #     history = history + "\n\n" + i + "\n\n" + blog + "\n\n"
    #     content.append(x)
    # conclusion = "conclusion"
    # return content, introduction, conclusion
    



# def generate_image_e_3(prompt_in,file_name):
#     response = client.images.generate(
#     model="dall-e-3",
#     prompt=prompt_in,
#     size='1024x1024',
#     quality='standard',
#     style='vivid',
#     n=1,
#     )

#     image_url = response.data[0].url
#     time.sleep(2)
#     img_data = requests.get(image_url).content
#     with open('output/'+file_name+'.jpg', 'wb') as handler:
#         handler.write(img_data)

def get_response_from_openai_gpt3_5(prompt_in):
  try:

    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      messages=[
        {
          "role": "user",
          "content": prompt_in
        }
      ],
      temperature=1,
      max_tokens=3000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].message.content
  except Exception as e:
    print(e)

def get_response_from_openai_gpt4(prompt_in):
  try:

    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {
          "role": "user",
          "content": prompt_in
        }
      ],
      temperature=1,
      max_tokens=3000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].message.content
  except Exception as e:
    print(e)

def get_titles_based_on_keyword(prompt_in,main_key,sub_key):
    try:
        prompt_final=prompt_in.format(main_key,sub_key)
        res=get_response_from_openai_gpt4(prompt_final)
        print(res)
        start_index = res.find('[') + 1  
        end_index = res.find(']')
        list_str = res[start_index:end_index]
        result_list = [item.strip().strip('"').strip("'") for item in list_str.split(',')]
        return result_list

    except:
        return "open ai error"

def get_google_serach(key_word):
    headers = { 
    "apikey": "007721a0-c73e-11ee-a13b-01bde3732e95"}

    params = (
    ("q",key_word),
    ("location","New York,New York,United States"),)

    response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
    return response.text
