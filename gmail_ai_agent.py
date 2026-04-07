<<<<<<< HEAD
import base64
import os
import pickle
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from myenv.tasks import decide_action


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def authenticate():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def get_emails(service):
    results = service.users().messages().list(
        userId='me',
        maxResults=5,
        labelIds=['INBOX']
    ).execute()

    return results.get("messages", [])


def read_email(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id).execute()

    headers = msg['payload']['headers']

    subject = ""
    sender = ""

    for h in headers:
        if h["name"] == "Subject":
            subject = h["value"]
        if h["name"] == "From":
            sender = h["value"]

    return subject, "", sender


def extract_email(sender):
    if "<" in sender:
        return sender.split("<")[1].replace(">", "")
    return sender


def move_to_spam(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={
            'addLabelIds': ['SPAM'],
            'removeLabelIds': ['INBOX']
        }
    ).execute()


def send_reply(service, sender, text):
    to_email = extract_email(sender)

    if not to_email:
        return "No email found"

    msg = MIMEText(text)
    msg['to'] = to_email
    msg['subject'] = "Re: Auto Reply"

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return f"Replied to {to_email}"


def run_agent():
    output = []

    service = authenticate()

    emails = get_emails(service)

    if not emails:
        return "No emails found"

    for e in emails:
        msg_id = e["id"]

        subject, body, sender = read_email(service, msg_id)

        action = decide_action(subject, body)

        output.append(f"Subject: {subject}")
        output.append(f"From: {sender}")
        output.append(f"Decision: {action.action_type} - {action.label}")

        if action.action_type == "move":
            move_to_spam(service, msg_id)
            output.append("Moved to spam")

        elif action.action_type == "respond":
            result = send_reply(service, sender, action.response_text)
            output.append(result)

        elif action.action_type == "ignore":
            output.append("Ignored")

        output.append("------------------------------------")

    return "\n".join(output)


if __name__ == "__main__":
=======
import base64
import os
import pickle
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from myenv.tasks import decide_action


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def authenticate():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def get_emails(service):
    results = service.users().messages().list(
        userId='me',
        maxResults=5,
        labelIds=['INBOX']
    ).execute()

    return results.get("messages", [])


def read_email(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id).execute()

    headers = msg['payload']['headers']

    subject = ""
    sender = ""

    for h in headers:
        if h["name"] == "Subject":
            subject = h["value"]
        if h["name"] == "From":
            sender = h["value"]

    return subject, "", sender


def extract_email(sender):
    if "<" in sender:
        return sender.split("<")[1].replace(">", "")
    return sender


def move_to_spam(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={
            'addLabelIds': ['SPAM'],
            'removeLabelIds': ['INBOX']
        }
    ).execute()


def send_reply(service, sender, text):
    to_email = extract_email(sender)

    if not to_email:
        return "No email found"

    msg = MIMEText(text)
    msg['to'] = to_email
    msg['subject'] = "Re: Auto Reply"

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return f"Replied to {to_email}"


def run_agent():
    output = []

    service = authenticate()

    emails = get_emails(service)

    if not emails:
        return "No emails found"

    for e in emails:
        msg_id = e["id"]

        subject, body, sender = read_email(service, msg_id)

        action = decide_action(subject, body)

        output.append(f"Subject: {subject}")
        output.append(f"From: {sender}")
        output.append(f"Decision: {action.action_type} - {action.label}")

        if action.action_type == "move":
            move_to_spam(service, msg_id)
            output.append("Moved to spam")

        elif action.action_type == "respond":
            result = send_reply(service, sender, action.response_text)
            output.append(result)

        elif action.action_type == "ignore":
            output.append("Ignored")

        output.append("------------------------------------")

    return "\n".join(output)


if __name__ == "__main__":
>>>>>>> cba4c8e (removed pycache folders)
    print(run_agent())