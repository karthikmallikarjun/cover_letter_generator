import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chain import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cover Letter Generator")
    url_input = st.text_input("Enter the URL of the job description:", 
                              value="https://www.stepstone.de/stellenangebote--Product-Owner-Product-Data-Management-and-Presentation-m-f-d-Muenchen-Jochen-Schweizer-mydays-Holding-GmbH--12317502-inline.html?rltr=1_1_25_seorl_m_0_0_0_0_1_0")
    submit_button_english = st.button("Generate Cover Letter in English")
    submit_button_german = st.button("Generate Cover Letter in German")

    if submit_button_english:
        st.code("Generating cover letter in English...")
        try:
            loader = WebBaseLoader([url_input])
            #Get the data from the web page for the job posting and clean it
            data = loader.load().pop().page_content
            #Load the details from the resume.csv file
            portfolio.load_portfolio()
            #Extract the job details and parse in a json format
            jobs = llm.extract_jobs(data)
            links = portfolio.query_links(jobs)
            email = llm.write_mail_english(jobs, links)
            #st.code(email, language='markdown')
            st.text_area("Code Block", email, height=800)
            st.code("Cover letter generated successfully.")

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

    elif submit_button_german:
        st.code("Generating cover letter in German...")
        try:
            loader = WebBaseLoader([url_input])
            data = loader.load().pop().page_content
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)   
            links = portfolio.query_links(jobs)
            email = llm.write_mail_german(jobs, links)
            st.text_area("Code Block", email, height=800)
            st.code("Cover letter generated successfully.")
    
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    # Initialize the LLM and Portfolio
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(page_title="Cover Page Generator",page_icon="🧊", layout="wide",initial_sidebar_state="expanded",
                menu_items={
                    'Get Help': 'https://www.google.com/',
                    'Report a bug': "https://www.google.com/",
                    'About': "# This is a header. This is an *extremely* cool app!"
                    })
    create_streamlit_app(chain, portfolio, clean_text)
