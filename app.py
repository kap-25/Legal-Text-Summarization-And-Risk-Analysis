import os
import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import PyPDF2
from transformers import pipeline
import requests  # For making HTTP requests

# Load environment variables
load_dotenv()

# Google Sheets API setup
SERVICE_ACCOUNT_FILE = os.getenv("path_to_your_service_account_file.json")  # Path to your service account JSON file from environment variable
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
sheets_service = build("sheets", "v4", credentials=credentials)

# Email setup (if using an email service)
EMAIL_API_URL = os.getenv("EMAIL_API_URL")  # Email service API URL from environment variables
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")  # Email service API key from environment variables

def main():
    st.title("📄 Legal Assistance Chat")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload Legal Doc", type=["pdf"])

    if uploaded_file:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF content successfully uploaded and processed!")

        summary, risks_df = perform_analysis(pdf_text)

        # Create a DataFrame for results
        data = {
            "Section": ["Summary", "Risk Assessment"],
            "Details": [summary, risks_df.to_dict(orient='records')]
        }
        df = pd.DataFrame(data)
        st.write("### Processed Data", df)

        spreadsheet_id = upload_to_google_sheets(df)

        # Generate Google Sheets link
        sheets_link = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        st.success(f"Data successfully uploaded to Google Sheets: [Open Sheet]({sheets_link})")

        send_email_notification(sheets_link)

def extract_text_from_pdf(uploaded_file):
    """Extract text from the uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return "".join([page.extract_text() for page in pdf_reader.pages])

def perform_analysis(pdf_text):
    """Perform summarization and risk assessment on the PDF text."""
    summarization_pipeline = pipeline("summarization")
    summary = summarization_pipeline(pdf_text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    
    # Load risk analysis DataFrame from the Jupyter notebook file
    risks_df = pd.read_json('Risk assessment.ipynb') 

    return summary, risks_df

def upload_to_google_sheets(df):
    """Upload the DataFrame to Google Sheets and return the spreadsheet ID."""
    spreadsheet_body = {
        "properties": {"title": "Legal Document Analysis"}
    }
    spreadsheet = sheets_service.spreadsheets().create(
        body=spreadsheet_body, fields="spreadsheetId"
    ).execute()
    spreadsheet_id = spreadsheet.get("spreadsheetId")

    # Write DataFrame to Google Sheets
    sheet_values = [df.columns.values.tolist()] + df.values.tolist()
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Sheet1",
        valueInputOption="RAW",
        body={"values": sheet_values},
    ).execute()

    return spreadsheet_id

def send_email_notification(sheets_link):
    """Send an email notification with the link to the Google Sheets using an email service."""
    recipient_email = st.text_input("Enter recipient email for notification:", "")
    
    if st.button("Send Email Notification"):
        try:
            # Prepare email data
            email_data = {
                "to": recipient_email,
                "subject": "Legal Document Analysis Report",
                "body": f"Hello,\n\nThe legal document analysis report has been processed. You can view the details here: {sheets_link}\n\nBest regards,\nLegal Assistance Team"
            }

            # Send email using a POST request to the email service API
            response = requests.post(
                EMAIL_API_URL,
                json=email_data,
                headers={"Authorization": f"Bearer {EMAIL_API_KEY}"}
            )

            if response.status_code == 200:
                st.success("Email notification sent successfully!")
            else:
                st.error(f"Failed to send email: {response.text}")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

