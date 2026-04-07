<<<<<<< HEAD
from gmail_auth import authenticate_gmail

def get_emails():
    service = authenticate_gmail()

    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

        payload = msg_data['payload']
        headers = payload['headers']

        subject = ""
        sender = ""

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']

        print("\n📩 EMAIL")
        print("From:", sender)
        print("Subject:", subject)


if __name__ == "__main__":
=======
from gmail_auth import authenticate_gmail

def get_emails():
    service = authenticate_gmail()

    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

        payload = msg_data['payload']
        headers = payload['headers']

        subject = ""
        sender = ""

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']

        print("\n📩 EMAIL")
        print("From:", sender)
        print("Subject:", subject)


if __name__ == "__main__":
>>>>>>> cba4c8e (removed pycache folders)
    get_emails()