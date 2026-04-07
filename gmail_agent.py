<<<<<<< HEAD
from gmail_auth import authenticate_gmail
from myenv.models import Action
from inference import decide_action

import base64


def get_email_body(msg_data):
    try:
        parts = msg_data['payload'].get('parts', [])
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                return base64.urlsafe_b64decode(data).decode()
    except:
        return ""
    return ""


def run_agent():
    service = authenticate_gmail()

    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

        headers = msg_data['payload']['headers']
        subject, sender = "", ""

        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            if h['name'] == 'From':
                sender = h['value']

        body = get_email_body(msg_data)

        # Fake observation object
        class Obs:
            pass

        obs = Obs()
        obs.subject = subject
        obs.body = body

        action = decide_action(obs)

        print("\n📩 EMAIL")
        print("From:", sender)
        print("Subject:", subject)
        print("👉 AI Decision:", action.action_type, "-", action.label)

        # 🟢 TAKE ACTION
        if action.label == "spam":
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['INBOX']}
            ).execute()
            print("🚫 Marked as spam")

        elif action.label == "important":
            print("⭐ Important email (you can reply here later)")

        elif action.label == "personal":
            print("💬 Personal email")



if __name__ == "__main__":
=======
from gmail_auth import authenticate_gmail
from myenv.models import Action
from inference import decide_action

import base64


def get_email_body(msg_data):
    try:
        parts = msg_data['payload'].get('parts', [])
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                return base64.urlsafe_b64decode(data).decode()
    except:
        return ""
    return ""


def run_agent():
    service = authenticate_gmail()

    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

        headers = msg_data['payload']['headers']
        subject, sender = "", ""

        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            if h['name'] == 'From':
                sender = h['value']

        body = get_email_body(msg_data)

        # Fake observation object
        class Obs:
            pass

        obs = Obs()
        obs.subject = subject
        obs.body = body

        action = decide_action(obs)

        print("\n📩 EMAIL")
        print("From:", sender)
        print("Subject:", subject)
        print("👉 AI Decision:", action.action_type, "-", action.label)

        # 🟢 TAKE ACTION
        if action.label == "spam":
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['INBOX']}
            ).execute()
            print("🚫 Marked as spam")

        elif action.label == "important":
            print("⭐ Important email (you can reply here later)")

        elif action.label == "personal":
            print("💬 Personal email")



if __name__ == "__main__":
>>>>>>> cba4c8e (removed pycache folders)
    run_agent()