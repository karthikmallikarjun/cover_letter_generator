# 📧 Cover Letter  Generator
Cover Letter generator for applying to companies using groq, langchain and streamlit. It allows users to input the URL of a company's careers page. The tool then extracts job requirements and skills from that page and generates personalized email to the hiring manager in English and German. These letters include relevant Skills and experiences sourced from a vector database, based on the specific job descriptions and can be sent to the desired company over an email. 

**Imagine a scenario:**

- You are applying for a Data scientist role from the website stepstone. You copy the job link from the website and paste it, and click on generate letter in different languages, either German or english. Review the content of the email and it is ready to send to the manager. Happy Job Hunting!!
![img.png](imgs/img.png)

## Architecture Diagram
![img.png](imgs/architecture.png)

## Set-up
1. To get started we first need to get an API_KEY from here: https://console.groq.com/keys. Inside `app/.env` update the value of `GROQ_API_KEY` with the API_KEY you created. 


2. To get started, first install the dependencies using:
    ```commandline
     pip install -r requirements.txt
    ```
   
3. Run the streamlit app:
   ```commandline
   streamlit run app/main.py
   ```
   

**Additional Terms:**
This software is licensed under the MIT License. However, commercial use of this software is strictly prohibited without prior written permission from the author. Attribution must be given in all copies or substantial portions of the software.