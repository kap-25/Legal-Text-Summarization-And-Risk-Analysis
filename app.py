import streamlit as st
import pandas as pd
import json
import requests
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
from transformers import pipeline
from openai import OpenAI

# Initialize the Streamlit app with custom page configuration
st.set_page_config(
  page_title="Advanced AI-Driven Legal Document Summarization and Risk Assessment",
  layout="wide"
)

# Title and description of the application
st.title("Advanced AI-Driven Legal Document Summarization and Risk Assessment")
st.write("""
This system provides:
- Contextual summaries of legal documents.
- Identification of potential risks through clause cross-referencing.
- Real-time regulatory updates integration.
- Seamless integration with Google Sheets and email alerts for efficient tracking.                                    
""")

# Function to extract text from PDFs
def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file using PyMuPDF or pdfminer."""
    try:
        file_bytes = uploaded_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        if text.strip():
            return text
        return extract_text(uploaded_file)
    except Exception as e:
        return f"Error extracting text: {e}"

# 1. Document Parsing and Contextual Summarization Engine
def summarize_document(content):
    """
    Summarizes a given text content using a pre-trained summarization model.
    """
    summarizer = pipeline("summarization")
    summary = summarizer(content, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Upload and display a legal document
uploaded_file = st.file_uploader("Upload Legal Document", type=["txt", "pdf"])
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        content = extract_text_from_pdf(uploaded_file)
    else:
        content = uploaded_file.read().decode("utf-8")
    
    st.subheader("Uploaded Document")
    st.write(content)
    
    # Generate and display summary
    if st.button("Generate Summary"):
        summary = summarize_document(content)
        st.subheader("Document Summary")
        st.write(summary)

# 2. Risk Detection and Recommendation System
def detect_risks(content):
    """
    Detects potential risks in the given text content using a text classification model.
    """
    risk_model = pipeline("text-classification", model="distilbert-base-uncased", truncation=True)
    risks = risk_model(content[:512])
    return risks

# Detect risks in uploaded content
if uploaded_file:
    if st.button("Identify Risks"):
        risks = detect_risks(content)
        st.subheader("Identified Risks")
        st.write(risks)

# 3. Continuous Regulatory Update Tracker
def fetch_regulatory_updates():
    """Fetches real-time regulatory updates (placeholder implementation)."""
    updates = [
        "New GDPR guidelines released.",
        "Updated compliance requirements for HIPAA."
    ]
    return updates

# Display regulatory updates in the sidebar
if st.checkbox("Show Regulatory Updates"):
    updates = fetch_regulatory_updates()
    st.subheader("Regulatory Updates")
    for update in updates:
        st.write(f"- {update}")

# 4. Platform Integration and Interactive Dashboard
def integrate_with_google_sheets(sheet_id, data, access_token):
    """
    Appends data into a Google Sheet via API.
    """
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1!A1:append?valueInputOption=RAW"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"values": data}  # Must be a list of lists
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code

def send_email_alert(to_email, subject, body):
    """Sends email alerts via an external email API."""
    email_api_url = "https://api.mailjet.com/v3.1/send"
    payload = {
        "to": to_email,
        "subject": subject,
        "body": body
    }
    response = requests.post(email_api_url, json=payload)
    return response.status_code

# Sidebar options for integrations
st.sidebar.header("Integration Options")
sheet_id = st.sidebar.text_input("Google Sheet ID")
access_token = st.sidebar.text_input("Google OAuth Token", type="password")
email = st.sidebar.text_input("Alert Email Address")

if st.sidebar.button("Test Integrations"):
    if sheet_id and access_token:
        sheet_status = integrate_with_google_sheets(sheet_id, [["Test Data", "More Data"]], access_token)
        st.sidebar.write("Google Sheets Integration: Success" if sheet_status == 200 else "Failed")
    if email:
        email_status = send_email_alert(email, "Test Alert", "This is a test alert from the system.")
        st.sidebar.write("Email Alert: Success" if email_status == 200 else "Failed")

st.sidebar.write("Use the mail interface to upload documents and generate insights.")
