import os,re, json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            #model="deepseek-r1-distill-llama-70b",
            model="llama-3.3-70b-specdec",	
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.0)
        
    def extract_jobs(self, text):
        # Define the prompt template for extracting job details
        prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website which has the job posting details.
        Your job is to extract the job postings and return them in JSON format containing all the necessary information including the
        following keys: `role`, `experience`, `skills` , `employment type`, `location`  and `description` . Please add other keys if founds in the document and translate
        the text to english from any language received.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": text})
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Content too big, unable to parse.")
        return json_res
    

    def write_mail_english(self, jobs, links):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are XXX, a Data scientist with 8 years of industry experience in different domains of work. 
        You are applying for the job with the {job_description}.
        Your job is to write a cover in English in about 500 words to the recruiting manager of the job mentioned above describing your capability of fulfilling 
        their needs and your motivation to work fro the company. You can also give examples from the experience before to make it more 
        natural and effective. Also add the most relevant skill from the following skills to showcase your portfolio: {link_list}
        Remember you are XXX, a data scientist.
        Do not provide a preamble and the think block.
        ### EMAIL (NO PREAMBLE):              
        """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(jobs), "link_list": links[0] })
        return res.content

    def write_mail_german(self, jobs, links):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are XXX, a Data scientist with 8 years of industry experience in different domains of work. 
        You are applying for the job with the {job_description}.
        Your job is to write a cover in German in about 500 words to the recruiting manager of the job mentioned above describing your capability of fulfilling 
        their needs and your motivation to work fro the company. You can also give examples from the experience before to make it more 
        natural and effective. Also add the most relevant skill from the following skills to showcase your portfolio: {link_list}
        Remember you are XXX, a data scientist.
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):        
        """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(jobs), "link_list": links[0] })
        return res.content
            
