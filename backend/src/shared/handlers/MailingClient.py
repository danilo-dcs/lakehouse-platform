import resend
from shared.models.env import EnvSettings

class MailingClient:
    def __init__(self, sender_email:str = None):

        settings = EnvSettings()

        self.resend_api_key = settings.EMAIL_SERVICE_KEY        
        resend.api_key = self.resend_api_key

        self.sender_email = sender_email if sender_email else "noreply@lakehouse-app.pathotrack.health"
        self.subject = None
        self.text_body = None
        self.html_body = None

    def add_subject(self, subject: str):
        self.subject = subject
        return self

    def add_text_body(self, text: str):
        self.text_body = text
        return self

    def add_html_body(self, html: str):
        self.html_body = html
        return self

    def send_email(self, receiver_address: str) -> bool:
        # Build the email
        message = dict()
        message['from'] = f"Lakehouse App <{self.sender_email}>"
        message['to'] = receiver_address
        message['subject'] = self.subject or 'Data Lakehouse App Requires Action'

        if self.html_body:
            message['html'] = self.html_body

        if self.text_body:
            message["text"] = self.text_body

        try:
            _ = resend.Emails.send(message)
            return True
        
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
