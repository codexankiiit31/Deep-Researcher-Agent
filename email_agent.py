import os
from dotenv import load_dotenv
from typing import Dict
from clarifier_agent import get_gemini_model

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

# Load environment variables
load_dotenv(override=True)

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    from_email = Email(os.getenv("Ankitttx32@gmail.com"))  # must be verified in SendGrid
    to_email = To(os.getenv("Ankitmahule88@gmail.com"))         # recipient
    content = Content("text/html", html_body)

    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print("Email response:", response.status_code)
    return {"status": "success", "code": response.status_code}

INSTRUCTIONS = """
You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email,
providing the report converted into clean, well presented HTML with an appropriate subject line.
"""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=get_gemini_model(),
)
