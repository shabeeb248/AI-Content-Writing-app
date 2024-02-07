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
from prompts import *

openai.api_key = "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"
os.environ['OPENAI_API_KEY'] = "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"

#https://zenserp.com/thank-you-Free/
client = openai

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
    "apikey": "c200c400-c4b8-11ee-b984-31f4e259c81c"}

    params = (
    ("q",key_word),
    ("location","New York,New York,United States"),)

    response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
    return response.text

xy="""
{
    "query": {
        "q": "mobile phones",
        "location": "New York,New York,United States",
        "url": "https://www.google.com/search?q=mobile+phones&oq=mobile+phones&uule=w+CAIQICIfTmV3IFlvcmssTmV3IFlvcmssVW5pdGVkIFN0YXRlcw&hl=en&gl=us&sourceid=chrome&ie=UTF-8"
    },
    "organic": [
        {
            "position": 1,
            "title": "New Cell Phones for Sale | Buy Smartphones ...",
            "url": "https://www.t-mobile.com/cell-phones",
            "destination": "https://www.t-mobile.com › cell-phones",
            "description": "Explore T-Mobile's selection of the latest cell phones and smartphones. Compare models, prices, and features from the most popular brands today!",
            "isAmp": false
        },
        {
            "position": 2,
            "title": "Cell Phones: Smartphones and Mobile ... - Best Buy",
            "url": "https://www.bestbuy.com/site/electronics/mobile-cell-phones/abcat0800000.c?id=abcat0800000",
            "destination": "https://www.bestbuy.com › site › abcat0800000",
            "description": "Shop Best Buy for cell phones. Text, call and search the web with mobile phones from popular brands. Browse our selection to find the best smartphone for ...",
            "isAmp": false
        },
        {
            "position": 3,
            "title": "Unlocked Phones - Cheap Cell Phones",
            "url": "https://www.usmobile.com/shop",
            "destination": "https://www.usmobile.com › shop",
            "description": "US Mobile is a prepaid carrier with the best cell phone plans and unlocked phones. The average monthly phone bill is $15. No contract or credit check ...",
            "isAmp": false
        },
        {
            "position": 4,
            "title": "Mobile phone",
            "url": "https://en.wikipedia.org/wiki/Mobile_phone",
            "destination": "https://en.wikipedia.org › wiki › Mobile_phone",
            "description": "A mobile phone (or cellphone) is a portable telephone that can make and receive calls over a radio frequency link while the user is moving within a ...",
            "isAmp": false
        },
        {
            "position": 5,
            "title": "Mint Mobile Phones for Sale",
            "url": "https://phones.mintmobile.com/",
            "destination": "https://phones.mintmobile.com",
            "description": "Buy a new phone or upgrade your current phone today at the Mint Mobile Phone Store. Get low monthly payments as low as 0% APR for up to 24 months.",
            "isAmp": false
        },
        {
            "position": 6,
            "title": "Cell Phones, Unlocked & No - Walmart",
            "url": "https://www.walmart.com/cp/cell-phones/1105910",
            "destination": "https://www.walmart.com › cell-phones",
            "description": "Looking for new cell phones? Shop for new cell phones, iPhones, unlocked phones, iPhone accessories, contract mobile phones and more Walmart.com.",
            "isAmp": false
        },
        {
            "position": 7,
            "title": "Cell Phones: Shop the Top Smartphones Online",
            "url": "https://www.verizon.com/smartphones/",
            "destination": "https://www.verizon.com › smartphones",
            "description": "At Verizon, you can browse your pick of smartphones and available deals on top brands, as well as explore the best cell phone service plans for your needs.",
            "isAmp": false
        },
        {
            "position": 8,
            "title": "Phones | SimpleMobile",
            "url": "https://shop.simplemobile.com/shop/en/simplemobile/phones",
            "destination": "https://shop.simplemobile.com › shop › phones",
            "description": "... Mobile Unlimited Mobile No Contract Cell Phone Plans. PHONES · PLANS ... phone catalog and see your EXCLUSIVE offers. Go to phones. UPGRADE YOUR PHONE. SORRY, You ...",
            "isAmp": false
        },
        {
            "position": 9,
            "title": "See New Android Phones & Prices",
            "url": "https://www.t-mobile.com/cell-phones/osy/android",
            "destination": "https://www.t-mobile.com › cell-phones › osy › android",
            "description": "Find the latest Android phones at T-Mobile, and compare different models, prices, features, and more. Get FREE SHIPPING on phones and devices with new ...",
            "isAmp": false
        }
    ],
    "related_searches": [
        {
            "title": "t-mobile phones",
            "url": "https://www.google.com/search?sca_esv=a6fbe16d171ab0fd&hl=en&gl=us&q=T-Mobile+phones&sa=X&ved=2ahUKEwjKz_qWkJaEAxUyRaQEHYnrDWsQ1QJ6BQiGARAB"
        },
        {
            "title": "10 uses of mobile phones",
            "url": "https://www.google.com/search?sca_esv=a6fbe16d171ab0fd&hl=en&gl=us&q=10+uses+of+mobile+phones&sa=X&ved=2ahUKEwjKz_qWkJaEAxUyRaQEHYnrDWsQ1QJ6BQiIARAB"
        },
        {
            "title": "history of mobile phones 1973 to 2017",
            "url": "https://www.google.com/search?sca_esv=a6fbe16d171ab0fd&hl=en&gl=us&q=History+of+mobile+phones+1973+to+2017&sa=X&ved=2ahUKEwjKz_qWkJaEAxUyRaQEHYnrDWsQ1QJ6BQiKARAB"
        },
        {
            "title": "us mobile phones",
            "url": "https://www.google.com/search?sca_esv=a6fbe16d171ab0fd&hl=en&gl=us&q=US+Mobile+phones&sa=X&ved=2ahUKEwjKz_qWkJaEAxUyRaQEHYnrDWsQ1QJ6BQiHARAB"
        },
        {
            "title": "who invented mobile phone in which year",
            "url": "https://www.google.com/search?sca_esv=a6fbe16d171ab0fd&hl=en&gl=us&q=Who+invented+mobile+phone+in+which+year&sa=X&ved=2ahUKEwjKz_qWkJaEAxUyRaQEHYnrDWsQ1QJ6BQiDARAB"
        },
        {
            "title": "unlocked mobile phones",
            "url": "https://www.google.com/search?sca_esv=a6fbe16d171ab0fd&hl=en&gl=us&q=Unlocked+Mobile+phones&sa=X&ved=2ahUKEwjKz_qWkJaEAxUyRaQEHYnrDWsQ1QJ6BQiCARAB"
        }
    ],
    "number_of_results": 1920000000
}

"""
# Initialize session state variables


if 'keyword_input' not in st.session_state:
  st.session_state["keyword_input"]=''


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

st.markdown("<h1 style='text-align: center; color: white;'>AI Content Creator App</h1>", unsafe_allow_html=True)


st.session_state["keyword_input"] = st.text_input("Enter a keyword")



if not st.session_state["keyword_input"]:
        st.error("Please fill out the keyword field")
else:
    # data=get_google_serach(st.session_state["keyword_input"])
    data = json.loads(xy)

    google_keywords=[]
    for item in data['organic']:
        google_keywords.append(item['title'])

    for search in data['related_searches']:
       google_keywords.append(search['title'])

    for item in google_keywords:
        if st.checkbox(item, key=item):
            st.session_state['selected_items'].append(item)

# if not st.session_state['selected_items']:
#         st.error("Please select multiple keywords")
# else:
#     if st.button('Submit'):
#         # titles_10=get_titles_based_on_keyword(prompt_1,st.session_state["keyword_input"],st.session_state['selected_items'])
#         titles_10=["1. Get More for Less: Top 10 Unlocked Mobile Phones You Can Buy Today", 
# "2. Discover 7 Unexpected Uses of Mobile Phones Beyond Calling and Texting", 
# "3. A Guide to Buying the Best New Cell Phones for Sale: Your Key to Evolving Tech", 
# "4. Score Big Savings with These Cheap Mobile Phones", 
# "5. Top 5 Hot Mint Mobile Phones for Sale: Why They are Worth Your Money", 
# "6. Unlocked Phones - The Future of Mobile Phone Ownership?", 
# "7. 'Cheap Mobile Phones' - Just a Myth or Reality?", 
# "8. Mint Mobile Phones: The Perfect Blend of Affordability and Functionality?", 
# "9. 12 Handy Uses of Mobile Phones That Will Change Your Life", 
# "10. How to Make the Most Out of the New Cell Phones for Sale Offerings"]
#         if isinstance(titles_10, list):
#           st.session_state['selected_titles']=titles_10

# if not st.session_state['selected_titles']:
#         st.error("Please select multiple keywords")
# else:          
#     list_titles=st.session_state['selected_titles']
#     for titl in list_titles:
   
#         if st.checkbox(titl, key=titl):
#             st.session_state['selected_titles'].append(titl)


# if st.session_state['selected_titles']:
#             if st.button('Submit123'):
#                 st.write(st.session_state['selected_titles'][0])   

   
# Initialize selected_titles in session_state if not already present
if 'selected_titles' not in st.session_state:
    st.session_state['selected_titles'] = []

if not st.session_state.get('selected_items', []):
    st.error("Please select multiple keywords")
else:
    if st.button('Submit'):
        titles_10 = [
            "1. Get More for Less: Top 10 Unlocked Mobile Phones You Can Buy Today",
            "2. Discover 7 Unexpected Uses of Mobile Phones Beyond Calling and Texting",
            "3. A Guide to Buying the Best New Cell Phones for Sale: Your Key to Evolving Tech",
            # ... other titles omitted for brevity
        ]
        # Directly set selected_titles to titles_10 instead of appending
        st.session_state['selected_titles'] = titles_10

# Checking for 'selected_titles' existence and non-emptiness
if st.session_state.get('selected_titles'):
    # Temporary list to store newly selected titles
    new_selected_titles = []
    
    # Iterate with index for unique keys
    for index, title in enumerate(st.session_state['selected_titles']):
        # Use index in the key to ensure uniqueness
        if st.checkbox(title, key=f"title_{index}"):
            new_selected_titles.append(title)
    
    # Update session_state with newly selected titles
    st.session_state['selected_titles'] = new_selected_titles

    if st.button('Finalize Selection'):
        # Example action: Display first selected title or a custom message if none are selected
        first_title = st.session_state['selected_titles'][0] if st.session_state['selected_titles'] else 'No titles selected.'
        st.write(first_title)



      

            




    


#     if st.button("TRANSLATE") or st.session_state['button_clicked']:
#       st.session_state['button_clicked'] = True
#       with st.spinner('TRANSLATING...'):
#         for file in uploaded_files:
#             bytes_data =file.read()
#             with open("input_folder/"+file.name,"wb") as f:
#                 f.write(bytes_data)
#         if st.session_state['model'] and st.session_state['languages'] and st.session_state['folder_name']:

#             num_langs = len(st.session_state['languages'])
#             prg = st.progress(0,"0 %")

                       
#             current_iteration = 0
#             total_iterations = num_files * num_langs
#             for lang_index,lang in enumerate(st.session_state['languages']):


#                 lan_code=get_language_code(lang) 
#                 create_subfolder("output_folder", st.session_state['folder_name']+"-"+lan_code)

#                 for file_index,file in enumerate(uploaded_files):
#                     doc_text = read_docx("input_folder/"+file.name)
#                     chunks_list=split_into_chunks(doc_text)
#                     final_res=""
#                     for i in chunks_list:
#                         prompt_filled = prompt_base.format(lang, lang, lang, lang, i)
#                         if st.session_state['model']=="gpt-3.5":
#                             res=get_response_from_openai_gpt3_5(prompt_filled)
#                         else:
#                             res=get_response_from_openai_gpt4(prompt_filled)

#                         final_res=final_res+res

#                     document = Document()
#                     document.add_paragraph(final_res)
#                     out_file_name= file.name.replace("EN", lan_code)
#                     document.save("output_folder/"+st.session_state['folder_name']+"-"+lan_code+"/"+out_file_name)
#                     current_iteration += 1
#                     per = (current_iteration / total_iterations) * 100 - 2
#                     per=round(per,1)
#                     prg.progress(per/100,text=str(per)+"%")

#             st.session_state['button_clicked'] = False
#             st.session_state['languages'] = []
#             st.session_state['folder_name'] = ''



#             folder_to_zip = "output_folder"  
#             zip_path = zip_folder(folder_to_zip, 'Output')

#             prg.progress(1.0,text="100 %")
#             st.balloons()
#             st.write("TRANSLATION COMPLETED !!!!!")
#             with open(zip_path, 'rb') as file:
#                 st.download_button(
#                     label='Download ZIP',
#                     data=file,
#                     file_name='Output.zip',
#                     mime='application/zip'
#                 )


# deleteOutput("input_folder")
# deleteOutput("output_folder")
# if os.path.exists("Output.zip"):
#     os.remove("Output.zip")

