import streamlit as st



st.set_page_config(page_title="AI Content Creator App", layout="wide",page_icon="🤖")
st.markdown("<h1 style='text-align: center; color: White;'>Welcome to AI Content Creator App</h1>", unsafe_allow_html=True)


css = """
<style>
    .stApp {
        background: Black;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .header {
        background-color: black; /* White background for the header */
        color: white; /* Black text for the header */
        text-align: center;
        font-size: 2.5em;
        padding: 10px;
        border-radius: 10px;
    }
    .sub-header, .content {
        color: white; /* White text for sub-header and content */
        text-align: center;
        font-size: 1.2em;
    }
    .content {
        font-size: 1.1em;
    }
</style>
"""


st.markdown(css, unsafe_allow_html=True)

# Introduction image for Debate-AI
st.image('img_1.png',  use_column_width='always')


st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: left; color: White;'>Easily Generate Content using GPT models</h2>", unsafe_allow_html=True)

st.markdown("""
    <style>
        .content p {
            text-align: left;
            font-size:20px;
            color:#05E5DF;
        }
    </style>
    <div class="content">
        <p><i class="fa-solid fa-upload"></i>-> Input any keywords to receive relevant SEO keywords from Google.</p>
        <p><i class="fas fa-cogs icon"></i>-> Obtain the relevant SEO keywords.</p>
        <p><i class="fas fa-folder-plus icon"></i>-> Select the keywords you desire.</p>
        <p><i class="fas fa-folder-plus icon"></i>-> Generate a title for the article.</p>
        <p><i class="fas fa-folder-plus icon"></i>-> Generate subheadings for the article.</p>
        <p><i class="fas fa-folder-plus icon"></i>-> Create content for each subheading of the article.</p>
        <p><i class="fas fa-folder-plus icon"></i>-> Download the final article.</p>

    </div>
    """, unsafe_allow_html=True)




