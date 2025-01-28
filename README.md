# Legal-Text-Summarization-And-Risk-Analysis
An AI-powered tool for summarizing legal documents and identifying potential risks.

This project provides a web application for analyzing legal documents. Users can upload a PDF legal document, and the system will process it by extracting text, summarizing the content, and performing risk analysis. The results are then uploaded to Google Sheets, and an email notification is sent to the specified recipient.

Features:

  - Upload a PDF document for analysis
  - Extract and summarize the document's content
  - Perform a risk assessment on the document
  - Upload the processed data to Google Sheets
  - Send email notifications with the results

Requirements:

  - Python 3.7 or higher
  - requirements.txt dependencies

Installation:

  1] Clone the repository:
  
      git clone https://github.com/kap-25/Legal-Text-Summarization-And-Risk-Analysis
      cd Legal-Text-Summarization-And-Risk-Analysis

  2] Install the required Python packages:
  
      pip install -r requirements.txt

  3] Set up environment variables:
      Create a .env file in the project root directory and add the following environment variables:
      
        SERVICE_ACCOUNT_FILE=path_to_your_service_account_file.json
        EMAIL_API_URL=your_email_service_api_url
        EMAIL_API_KEY=your_email_service_api_key

  4] To obtain the SERVICE_ACCOUNT_FILE for Google Sheets API, follow the Google Sheets API documentation and create a service account. Make sure to grant it access to your Google Sheets.

Usage:

  1] Run the Streamlit app:
  
      streamlit run app.py

  2] The app will start, and you will be able to upload a PDF document for analysis. Once uploaded, the system will:
      - Extract text from the PDF
      - Summarize the content using NLP techniques
      - Perform a risk assessment (using a pre-defined risk model)
      - Upload the results to Google Sheets
      - Send an email notification with the link to the Google Sheet

Project Structure:

  - app.py: Main Streamlit application
  - requirements.txt: Python dependencies
  - README.md: This file

Dependencies:

  - streamlit: For building the web interface.
  - pandas: For data manipulation.
  - google-api-python-client: To interact with the Google Sheets API.
  - google-auth: For authenticating with Google services.
  - python-dotenv: To load environment variables from .env.
  - PyPDF2: For extracting text from PDF files.
  - transformers: For using pre-trained machine learning models for summarization.
  - requests: For sending HTTP requests, including email notifications.
